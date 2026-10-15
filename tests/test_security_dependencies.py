"""Offline regression coverage for patched dependencies and application authentication."""
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import jwt
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[1]


class DependencySecurityTests(unittest.TestCase):
    def test_all_exported_runtime_pins_match_lock(self):
        lock = json.loads((ROOT / 'Pipfile.lock').read_text(encoding='utf-8'))
        expected = {canonicalize_name(name): value['version'] for name, value in lock['default'].items()}
        exported = {}
        for line in (ROOT / 'requirements.txt').read_text(encoding='utf-8-sig').splitlines():
            if not line.strip() or line.startswith(('#', '-i ')):
                continue
            requirement = Requirement(line)
            exported[canonicalize_name(requirement.name)] = str(requirement.specifier)
        self.assertEqual(exported, expected)

    def test_patched_versions_match_both_manifests(self):
        lock = json.loads((ROOT / 'Pipfile.lock').read_text(encoding='utf-8'))
        requirements = (ROOT / 'requirements.txt').read_text(encoding='utf-8-sig').lower()
        for package, version in [('anyio', '4.14.2'), ('pyjwt', '2.15.0'), ('werkzeug', '3.1.9')]:
            self.assertEqual(lock['default'][package]['version'], '==' + version)
            self.assertIn(package + '==' + version, requirements)
            self.assertEqual(importlib.metadata.version(package), version)

    def test_signed_token_and_tampered_signature(self):
        key = 'offline-test-key-not-a-production-secret-12345'
        token = jwt.encode({'sub': 'smoke-user', 'exp': int(time.time()) + 60}, key, algorithm='HS256')
        self.assertEqual(jwt.decode(token, key, algorithms=['HS256'])['sub'], 'smoke-user')
        with self.assertRaises(jwt.InvalidSignatureError):
            jwt.decode(token, 'different-offline-key-12345678901234567890', algorithms=['HS256'])

    def test_unverified_peek_does_not_mutate_claim_options(self):
        key = 'offline-test-key-not-a-production-secret-12345'
        token = jwt.encode({'sub': 'expired-user', 'exp': int(time.time()) - 3600}, key, algorithm='HS256')
        options = {'verify_signature': False}
        jwt.decode(token, options=options)
        self.assertEqual(options, {'verify_signature': False})
        options['verify_signature'] = True
        with self.assertRaises(jwt.ExpiredSignatureError):
            jwt.decode(token, key, algorithms=['HS256'], options=options)


class ApplicationAuthenticationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='offline-tests-', dir=ROOT)
        cls.original_cwd = os.getcwd()
        os.chdir(cls.temp.name)
        sys.path.insert(0, str(ROOT / 'server'))
        # Never load a developer .env or connect to a real database/API in these tests.
        cls.environment = patch.dict(os.environ, {
            'OPENAI_API_KEY': 'offline-test-placeholder',
            'SECRET_KEY': 'offline-session-test-key-not-for-production',
            'DATABASE_URI': 'sqlite:///:memory:',
        })
        cls.environment.start()
        cls.dotenv = patch('dotenv.load_dotenv', return_value=False)
        cls.dotenv.start()
        cls.module = importlib.import_module('app')
        cls.app = cls.module.app
        cls.app.config['TESTING'] = True

    @classmethod
    def tearDownClass(cls):
        cls.dotenv.stop()
        cls.environment.stop()
        os.chdir(cls.original_cwd)
        cls.temp.cleanup()

    def setUp(self):
        with self.app.app_context():
            self.module.db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            self.module.db.session.remove()
            self.module.db.drop_all()

    def test_registration_login_logout_and_wrong_password(self):
        registered = self.client.post('/api/user_auth', json={
            'username': 'smokeuser', 'email': 'smoke@example.invalid', 'password': 'offline-password-123'
        })
        self.assertEqual(registered.status_code, 201)
        self.assertNotIn('password_hash', registered.get_json())
        self.assertEqual(self.client.post('/api/logout').status_code, 200)
        wrong = self.client.post('/api/login', json={'username': 'smokeuser', 'password': 'wrong-password'})
        self.assertEqual(wrong.status_code, 401)
        accepted = self.client.post('/api/login', json={'username': 'smokeuser', 'password': 'offline-password-123'})
        self.assertEqual(accepted.status_code, 200)
        with self.client.session_transaction() as session:
            self.assertTrue(session['logged_in'])
        self.client.post('/api/logout')
        with self.client.session_transaction() as session:
            self.assertNotIn('user_id', session)

    def test_reject_missing_login_and_anonymous_chat(self):
        self.assertEqual(self.client.post('/api/login', json={}).status_code, 400)
        self.assertEqual(self.client.post('/api/user_auth', json={}).status_code, 400)
        self.assertEqual(self.client.post('/api/chat_messages', json={'message': 'offline'}).status_code, 403)


if __name__ == '__main__':
    unittest.main()
