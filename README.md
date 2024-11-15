Authentication Middleware for Django application following OpenID connect. Built on top of drf-simeplejwt and Authlib

Add following settings to Django settings

INSTALLED_APPS = {
    ...,
    django_sso_client,
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