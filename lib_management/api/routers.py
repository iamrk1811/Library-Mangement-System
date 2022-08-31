from rest_framework import routers
from .viewsets import BookViewSet, MemberViewSet, SuperUserView
api_router = routers.DefaultRouter()


api_router.register('book', BookViewSet, basename="book")
api_router.register('member', MemberViewSet, basename="member")
api_router.register('superuser', SuperUserView, basename="superuser")
