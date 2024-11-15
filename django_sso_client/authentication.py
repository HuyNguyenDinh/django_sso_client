import datetime

from authlib.integrations.django_client import OAuth
from authlib.jose import JsonWebKey, jwt, JWTClaims
from django.core.cache import cache
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django_sso_client.settings  import settings
from django.contrib.auth import get_user_model

User = get_user_model()
oauth = OAuth()
oauth.register(
    name="sso",
    server_metadata_url=settings.METADATA
)

AUTH_HEADER_TYPES = settings.AUTH_HEADER_TYPES

AUTH_HEADER_TYPE_BYTES = set(
    h.encode(HTTP_HEADER_ENCODING)
    for h in AUTH_HEADER_TYPES
)

class SSOAuthentication(JWTAuthentication):

    def verify_token(self, jwt_claim: JWTClaims):
        try:
            jwt_claim.validate()
        except TokenError as e:
            raise AuthenticationFailed('Token invalid')
        except Exception as e:
            raise AuthenticationFailed(str(e))
        else:
            user = cache.get(settings.USER_CACHE_KEY_FORMAT.format(jwt_claim.jti))
            if not user:
                user = User(username=jwt_claim.get("preferred_username"))
                cache.set(settings.USER_CACHE_KEY_FORMAT.format(jwt_claim.jti), user, jwt_claim.exp - datetime.datetime.now().timestamp())
            return user

    def get_validated_token(self, raw_token) -> JWTClaims:
        jwk_set = cache.get(settings.PUBLIC_KEY.get("CACHE_KEY"))
        if not jwk_set:
            jwk_set = oauth.sso.fetch_jwk_set()
            cache.set(settings.PUBLIC_KEY.get("CACHE_KEY"), jwk_set, settings.PUBLIC_KEY.get("TTL"))
        key_set = JsonWebKey.import_key_set(jwk_set)
        try:
            return jwt.decode(raw_token, key_set)
        except Exception as e:
            raise InvalidToken({
                "detail": "Given token not valid for any token type",
                "message": str(e)
            })

    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                'Authorization header must contain two space-delimited values',
                code='bad_authorization_header',
            )

        return parts[1]

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.verify_token(validated_token), validated_token
