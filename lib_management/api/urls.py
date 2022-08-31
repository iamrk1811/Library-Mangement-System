from api.routers import api_router
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path(r'signup/', views.SignUpView.as_view(), name='signup'),
    path(r'login/', views.LoginView.as_view(), name='login'),
    path(r'logout/', views.Logout.as_view(), name='logout'),
    path(r'self_delete/', views.SelfDeleteMemberView.as_view(), name='self_delete_member'),
    path('', include(api_router.urls)),
]


