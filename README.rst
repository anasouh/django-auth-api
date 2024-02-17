================
django-auth-api
================

A simple Django app to provide a RESTful API for user authentication.

Quick start
-----------

1. Add "auth_api" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'django_auth_api',
    ]

2. Add DISPLAYED_NAME, PASSWORD_RESET_URL, EMAIL_HOST_USER to your settings.py like this::

    DISPLAYED_NAME = 'Your app name' # This will appear in the email sent to the user
    PASSWORD_RESET_URL = 'http://example.com/reset-password/' # This link will be sent with this parameter: ?token=<token>
    EMAIL_HOST_USER = 'noreply@example.com' # This will be the sender of the email

3. Include the auth_api URLconf in your project urls.py like this::

    path('api/', include('auth_api.urls')),

4. Run `python manage.py migrate` to create the auth_api models.

5. Start the development server