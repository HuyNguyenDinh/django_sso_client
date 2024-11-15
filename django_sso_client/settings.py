from django.conf import settings as django_settings

DEFAULT_SETTINGS = {
    "METADATA": "",
    "AUTH_HEADER_TYPES": ["Bearer"],
    "PUBLIC_KEY": {
        "CACHE_KEY": "sso:client:public_key",
        "TTL": 3600
    },
    "USER_CACHE_KEY_FORMAT": "sso:client:user:{}"
}

def get_settings():
    settings = getattr(django_settings, "SSO_CLIENT", {})
    for k, v in DEFAULT_SETTINGS.items():
        settings.setdefault(k, v)
    return settings

settings = get_settings()