"""Serializers for user registration and authentication."""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Serialize user registration data and create new user accounts.

    Validates username, email, and password fields. Ensures password
    confirmation matches and email uniqueness.
    """
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            }
        }

    def validate_confirmed_password(self, value):
        """Validate that password and confirmed_password match.

        Args:
            value: The confirmed_password field value

        Returns:
            str: The confirmed_password value if valid
        """
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value

    def validate_email(self, value):
        """Validate that email is not already registered.

        Args:
            value: The email field value

        Returns:
            str: The email value if unique
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        """Create and save new user with hashed password.

        Returns:
            dict: Success message confirming user creation
        """
        pw = self.validated_data['password']

        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        account.set_password(pw)
        account.save()
        return {
            "detail": "User created successfully!"
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serialize login credentials and return JWT tokens with user data.

    Extends simplejwt TokenObtainPairSerializer to include user information
    in the response.
    """
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Validate username and password credentials.

        Checks if user exists and password is correct, then generates
        JWT tokens.

        Args:
            attrs: Dictionary containing username and password

        Returns:
            dict: Validated data including tokens and user information
        """
        username = attrs.get('username')
        password = attrs.get('password')

        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError('Invalid username or password')
        data = super().validate({
            'username': user.username,
            'password': password
        })

        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        return data
