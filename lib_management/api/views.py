from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema
from rest_framework.views import APIView
from accounts.serializers import UserSerializer
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from accounts.decorators import member_access, login_required
from lib_management.utils import get_user_from_cookies

User = get_user_model()


class SignUpView(APIView):
    schema = ManualSchema(fields=[
        coreapi.Field(
            "first_name",
            required=True,
            schema=coreschema.String()
        ),
        coreapi.Field(
            "last_name",
            required=True,
            schema=coreschema.String()
        ),

        coreapi.Field(
            "email",
            required=True,
            schema=coreschema.String()
        ),
        coreapi.Field(
            "password",
            required=True,
            schema=coreschema.String()
        ),
        coreapi.Field(
            "user_type",
            required=True,
            schema=coreschema.Integer()
        ),
    ],
        description="Takes users credentials and create a user. \n User type: \n1 for - Librarian \n 2 for - Member"
    )

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class LoginView(APIView):
    schema = ManualSchema(fields=[
        coreapi.Field(
            "email",
            required=True,
            schema=coreschema.String()
        ),
        coreapi.Field(
            "password",
            required=True,
            schema=coreschema.String()
        ),
    ],
        description="Takes users credentials and return auth_token if user is authenticated"
    )

    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY , algorithm='HS256')

        response = Response()
        response.set_cookie(key="auth_token", value=token, httponly=True)

        response.data = {
            "Auth Token": token
        }

        response.status_code = status.HTTP_200_OK
        return response


class SelfDeleteMemberView(APIView):
    schema = ManualSchema( fields=[],
        description="Self delete a member"
    )
    @member_access
    def delete(self, request, *args, **kwargs):
        user = get_user_from_cookies(request.COOKIES)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND, data='Invalid user')
        user.delete()
        return Response(status=status.HTTP_200_OK, data="Deleted")


class Logout(APIView):
    schema = ManualSchema( fields=[],
        description="Logout"
    )

    @login_required
    def get(self, request):
        response = Response(status=status.HTTP_200_OK, data="Successfully Logged out")
        response.delete_cookie('auth_token')
        return response

