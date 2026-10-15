# Azure deployment template

`azure-webapps-python.json` is the existing Azure Resource Manager deployment template. It was previously stored with a `.yml` extension inside `.github/workflows`, where it was not a valid GitHub Actions workflow. Its contents are preserved here; moving it does not deploy Azure resources.

The separate Python security workflow checks both documented dependency installation paths, compares exported pins with the lockfile, exercises authentication offline using temporary SQLite/session data, and audits the runtime dependencies. Tests use placeholder credentials and make no OpenAI API requests.
