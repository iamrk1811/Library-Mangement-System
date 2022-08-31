from functools import wraps
import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.constants import UserType

User = get_user_model()


def login_required(func):
    @wraps(func)
    def wrapper(view, *args, **kwargs):
        auth_token = view.request.COOKIES.get('auth_token')
        if not auth_token:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")
        return func(view, *args, **kwargs)
    return wrapper


def librarian_access(func):
    @wraps(func)
    def wrapper(view, *args, **kwargs):
        auth_token = view.request.COOKIES.get('auth_token')
        if not auth_token:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")

        user = User.objects.filter(id=payload['id']).first()
        if user.user_type != UserType.LIBRARIAN:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")
        return func(view, *args, **kwargs)
    return wrapper


def member_access(func):
    @wraps(func)
    def wrapper(view, *args, **kwargs):
        auth_token = view.request.COOKIES.get('auth_token')
        if not auth_token:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")

        user = User.objects.filter(id=payload['id']).first()
        if user.user_type != UserType.MEMBER:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")
        return func(view, *args, **kwargs)
    return wrapper


def super_user_access(func):
    @wraps(func)
    def wrapper(view, *args, **kwargs):
        auth_token = view.request.COOKIES.get('auth_token')
        if not auth_token:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")

        user = User.objects.filter(id=payload['id']).first()
        if not user.is_superuser:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized Access")
        return func(view, *args, **kwargs)
    return wrapper


