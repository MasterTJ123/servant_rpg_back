from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from rest_framework import viewsets, status
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .permissions import IsOwnerUserOrIsAdminUser
from django.utils.translation import gettext_lazy as _


class LoginView(APIView):
    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            if not email:
                raise Exception(_("Email is required."))

            if not password:
                raise Exception(_("Password is required."))

            try:
                custom_user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise Exception(_("User not found."))

            if not custom_user.check_password(password):
                raise Exception(_("User not found."))

            refresh = RefreshToken.for_user(custom_user)
            # noinspection PyUnresolvedReferences
            access_token = refresh.access_token

            response = Response({"detail": _("Login successful.")}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='refresh_token', value=str(refresh), httponly=True, secure=False, samesite='Lax',
                max_age=refresh.lifetime
            )
            response.set_cookie(
                key='access_token', value=str(access_token), httponly=True, secure=False, samesite='Lax',
                max_age=access_token.lifetime
            )

            return response
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    def post(self):
        # Remover os cookies de tokens
        response = Response({"detail": _("Logged out.")}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')

        return response


class RefreshView(APIView):
    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            if not refresh_token:
                raise ValidationError(_("No refresh token provided."))

            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token

            response = Response({"detail": _("Token refreshed.")}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token', value=str(access_token), httponly=True, secure=False, samesite='Lax',
                max_age=access_token.lifetime
            )

            return response
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action in ('create', 'list'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsOwnerUserOrIsAdminUser]
        return [permission() for permission in permission_classes]

    def get_authenticators(self):
        if self.action not in ('create', 'list'):
            return [JWTAuthentication()]
        return []

    def list(self, request, *args, **kwargs):
        if IsAuthenticated().has_permission(request, self) and IsAdminUser().has_permission(request, self):
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response([])
