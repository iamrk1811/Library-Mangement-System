import jwt
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


def get_user_from_cookies(cookie):
    auth_token = cookie.get('auth_token', None)
    if not auth_token:
        return None
    try:
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None

    user = User.objects.filter(id=payload['id']).first()
    return user
