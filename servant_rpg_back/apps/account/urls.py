from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, LoginView, LogoutView, RefreshView


router = DefaultRouter()
router.register('users', CustomUserViewSet)

urlpatterns = [
    # Users
    path('', include(router.urls)),
    # Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
]
