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