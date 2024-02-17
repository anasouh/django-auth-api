# django-auth-api

A simple Django app to provide a RESTful API for user authentication.

## Quick start

1. Install the package using pip:

```sh
pip install git+https://github.com/anasouh/django-auth-api.git
```

2. Add "auth_api" to your INSTALLED_APPS setting like this::

```py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'django_auth_api',
]
```

3. Add DISPLAYED_NAME, PASSWORD_RESET_URL, EMAIL_HOST_USER to your settings.py like this::

```py
DISPLAYED_NAME = 'Your app name' # This will appear in the email sent to the user
PASSWORD_RESET_URL = 'http://example.com/reset-password/' # This link will be sent with this parameter: ?token=<token>
EMAIL_HOST_USER = 'noreply@example.com' # This will be the sender of the email
```

4. Include the auth_api URLconf in your project urls.py like this::

```py
path('api/', include('auth_api.urls')),
```

5. Run `python manage.py migrate` to create the auth_api models.

6. You can test the API using the command `python manage.py test django_auth_api`

7. Start the development server

## Endpoints

### User Login

- **URL:** `/api/auth/login/`
- **Method:** POST
- **Description:** This endpoint allows users to authenticate and obtain an authentication token for subsequent requests.
- **Permissions:** AllowAny
- **Request Body:**
  - `username` (string, required): The username of the user.
  - `password` (string, required): The password of the user.
- **Response:**
  - `token` (string): Authentication token for the user.
- **Status Codes:**
  - 200: OK (Login successful)
  - 400: Bad Request (If username or password is incorrect)

### Create a new user

- **URL:** `/api/auth/signup/`
- **Method:** POST
- **Description:** This endpoint allows the creation of a new user.
- **Permissions:** AllowAny
- **Request Body:**
  - `username` (string, required): The username of the new user.
  - `email` (string, required): The email of the new user.
  - `password` (string, required): The password of the new user.
- **Response:**
  - `token` (string): Authentication token for the newly created user.
- **Status Codes:**
  - 201: Created
  - 400: Bad Request

### User Logout

- **URL:** `/api/auth/logout/`
- **Method:** GET
- **Description:** This endpoint allows the user to log out.
- **Permissions:** TokenAuthentication
- **Request Headers:**
  - `Authorization: Token <token>`
- **Response:**
  - None
- **Status Codes:**
  - 200: OK (On successful logout)
  - 400: Bad Request (If the user is not authenticated)

### Verify Token

- **URL:** `/api/auth/token/verify/`
- **Method:** POST
- **Description:** This endpoint verifies the authenticity of a token.
- **Permissions:** AllowAny
- **Request Body:**
  - `token` (string, required): Token to be verified.
- **Response:**
  - None
- **Status Codes:**
  - 200: OK (Token is valid)
  - 400: Bad Request (Token is not valid)

### Request a password reset token by email

- **URL:** `/api/auth/password/reset/`
- **Method:** POST
- **Description:** This endpoint initiates the password reset process, the token has a validity of 30 minutes.
- **Permissions:** AllowAny
- **Request Body:**
  - `email` (string, required): Email of the user requesting password reset.
- **Response:**
  - None
- **Status Codes:**
  - 200: OK (Password reset initiated successfully)
  - 400: Bad Request (If email is not provided or invalid)

### Change password after reset

- **URL:** `/api/auth/password/reset/change/`
- **Method:** POST
- **Description:** This endpoint allows the user to change their password after a reset request.
- **Permissions:** AllowAny
- **Request Body:**
  - `token` (string, required): Token received for password reset.
  - `new_password` (string, required): New password to be set.
- **Response:**
  - None
- **Status Codes:**
  - 200: OK (Password changed successfully after reset)
  - 400: Bad Request (If token is invalid or expired)

### Authenticated user password change

- **URL:** `/api/auth/password/change/`
- **Method:** POST
- **Description:** This endpoint allows the user to change their password.
- **Permissions:** TokenAuthentication
- **Request Headers:**
  - `Authorization: Token <token`
- **Request Body:**
  - `old_password` (string, required): Current password of the user.
  - `new_password` (string, required): New password to be set.
- **Response:**
  - None
- **Status Codes:**
  - 200: OK (Password changed successfully)
  - 400: Bad Request (If old_password is incorrect or new_password is invalid)