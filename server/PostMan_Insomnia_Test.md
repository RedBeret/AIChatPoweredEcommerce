Create a New User:

Method: POST
URL: http://localhost:5555/user_auth
Body (JSON): {"username": "newUser", "email": "user@example.com", "password": "password123"}
Expected Success Response: Status 201, {"message": "User created successfully"}

Login:

Method: POST
URL: http://localhost:5555/login
Body (JSON): {"username": "newUser", "password": "password123"}
Expected Success Response: Status 200, with an access_token provided
!Capture that token for the next steps

Update Password (Ensure you're using the obtained JWT token for authorization):

Method: PATCH
URL: http://localhost:5555/user_auth (assuming this is your intended endpoint for password updates)
Headers: Authorization: Bearer <JWT_TOKEN>
- Type: Authorization
- Value: Bearer 1234567891234567987 
Body (JSON): {"username": "newUser", "password": "password123", "newPassword": "newPass456"}
Expected Success Response: Status 200, {"message": "Password updated successfully"}

Delete User (Using the new password for authentication):

Method: DELETE
URL: http://localhost:5555/user_auth (adjust if your endpoint is different)
Headers: Authorization: Bearer <JWT_TOKEN>
- Type: Authorization
- Value: Bearer 1234567891234567987 
Body (JSON): {"username": "newUser", "password": "newPass456"}
Expected Success Response: Status 200, {"message": "User deleted successfully"}
