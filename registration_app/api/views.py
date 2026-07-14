from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer, RegistrationSerializer
from .utils import set_auth_cookies, blacklist_refresh_token, clear_auth_cookies, set_access_cookie
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError


class RegistrationView(APIView):
    """Handle user registration endpoint.

    Accepts user credentials and creates a new user account.
    Validates input data and returns appropriate success/error responses.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user account.

        Validates the provided registration data (username, email, password)
        and creates a new user if validation succeeds.

        Args:
            request: HTTP request containing registration data

        Returns:
            Response: Success message with 201 status or validation errors
                with 400 status
        """
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenObtainPairView(TokenObtainPairView):
    """Handle user login and issue JWT tokens via HTTP-only cookies.

    Authenticates user credentials and returns JWT tokens stored in
    secure HTTP-only cookies to prevent XSS attacks.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """Authenticate user and set tokens in cookies.

        Validates username and password, generates JWT tokens, and stores
        them in secure HTTP-only cookies.

        Args:
            request: HTTP request containing username and password
            *args: Variable positional arguments
            **kwargs: Variable keyword arguments

        Returns:
            Response: Login success message with user data and tokens in
                secure HTTP-only cookies
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']
        user = serializer.validated_data.get('user')

        response = Response({
            'detail': 'Login successfully!',
            'user': user
        }, status=status.HTTP_200_OK)

        return set_auth_cookies(response, access, refresh)


class LogoutView(APIView):
    """Handle user logout and invalidate authentication tokens.

    Blacklists the refresh token and clears authentication cookies to
    securely log out users and prevent further token usage.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Log out user by invalidating tokens and clearing cookies.

        Retrieves refresh token from cookies, adds it to blacklist, and
        removes authentication cookies from the response.

        Args:
            request: HTTP request from authenticated user
            *args: Variable positional arguments
            **kwargs: Variable keyword arguments

        Returns:
            Response: Success message with status 200
        """
        refresh_token = request.COOKIES.get('refresh_token')
        blacklist_refresh_token(refresh_token)

        response = Response(
            {"detail": "Successfully logged out. Tokens have been deleted."},
            status=status.HTTP_200_OK
        )
        return clear_auth_cookies(response)


class CookieRefreshView(TokenRefreshView):
    """Handle token refresh using refresh token from cookies.

    Validates refresh token, generates new access token, and updates the
    access token cookie without requiring re-authentication.
    """

    def post(self, request, *args, **kwargs):
        """Refresh the access token using refresh token from cookies.

        Retrieves refresh token from cookies, validates it, generates
        a new access token, and updates the access token cookie.

        Args:
            request: HTTP request containing refresh token in cookies
            *args: Variable positional arguments
            **kwargs: Variable keyword arguments

        Returns:
            Response: New access token with 200 status or error with
                401 status if refresh token not found or invalid
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token not found in cookies'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(data={'refresh': refresh_token})
        serializer.is_valid(raise_exception=True)

        access_token = serializer.validated_data.get('access')
        response = Response(
            {'detail': 'Token refreshed'},
            status=status.HTTP_200_OK
        )
        return set_access_cookie(response, access_token)
