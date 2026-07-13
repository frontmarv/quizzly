from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer, RegistrationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenObtainPairView (TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']
        user = serializer.validated_data.get('user')

        response = Response({
            'detail': 'Login successfully!',
            'user': user
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=str(access),
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response


class LogoutView(APIView):
    """Loggt den User aus, entwertet den Cookie-Refresh-Token und löscht die Cookies."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs) -> Response:
        response = Response(
            {"detail": "Erfolgreich ausgeloggt. Tokens wurden gelöscht."},
            status=status.HTTP_200_OK
        )
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class CookieRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token not found in cookies'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data={'refresh': refresh_token})
        serializer.is_valid(raise_exception=True)

        access_token = serializer.validated_data.get('access')
        response = Response({'access': access_token},
                            status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        response.data = {
            "detail": "Token refreshed"}
        return response
