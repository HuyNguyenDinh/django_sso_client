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

class ClientSettings(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def get_settings():
    settings_dict = getattr(django_settings, "SSO_CLIENT", {})
    for k, v in DEFAULT_SETTINGS.items():
        settings.setdefault(k, v)
    settings = ClientSettings(**settings_dict)
    return settings

settings = get_settings()