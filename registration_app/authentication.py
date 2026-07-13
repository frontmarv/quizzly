from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication, die den Token aus Cookies liest,
    falls er nicht im Authorization Header vorhanden ist.
    """

    def authenticate(self, request):
        auth_header = self.get_header(request)

        if auth_header is None:
            raw_token = request.COOKIES.get('access_token')

            if raw_token is None:
                return None
        else:
            raw_token = self.get_raw_token(auth_header)
            if raw_token is None:
                return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except Exception:
            raise AuthenticationFailed("Invalid token in cookies")

        return self.get_user(validated_token), validated_token
