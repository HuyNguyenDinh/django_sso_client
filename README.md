# Authentication Middleware for Django Application

An authentication middleware for Django applications following OpenID Connect. Built on top of **drf-simplejwt** and **Authlib**.

## Configuration

### Add the following settings to your Django `settings.py`

#### 1. **Installed Apps**

```python
INSTALLED_APPS = {
    ...,
    'django_sso_client',
    ...
}

REST_FRAMEWORK = {
    ...,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...,
        'django_sso_client.authentication.SSOAuthentication',
        'your_custom_middleware',
        ...
    ),
    ...
}

SSO_CLIENT = {
    "METADATA": "http://localhost:8000/.well-known/openid-configuration",
    "AUTH_HEADER_TYPES": ["Bearer"],
    "PUBLIC_KEY": {
        "CACHE_KEY": "sso:client:public_key",
        "TTL": 3600
    },
    "USER_CACHE_KEY_FORMAT": "sso:client:user:{}"
}

AUTHLIB_OAUTH_CLIENTS = {
    'sso': {
        'client_id': 'client_id',
        "client_secret": 'client_secret',
    }
}
