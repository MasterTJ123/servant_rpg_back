from .models import CustomUser, Combatant, CombatantGroup, Group, Ambient, Encounter, EnemyEncounter
from .serializers import CustomUserSerializer, CombatantSerializer, AmbientSerializer, GroupSerializer, \
    CombatantGroupSerializer, EncounterSerializer, EnemyEncounterSerializer
from .permissions import IsOwnerUser
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.status import HTTP_200_OK
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
                key='refresh_token', value=str(refresh), httponly=True, secure=False, samesite=None,
                max_age=refresh.lifetime
            )
            response.set_cookie(
                key='access_token', value=str(access_token), httponly=True, secure=False, samesite=None,
                max_age=access_token.lifetime
            )

            return response
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic, PyUnusedLocal
    def post(self, request):
        response = Response({"detail": _("Logged out.")}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return response


class RefreshView(APIView):
    permission_classes = [IsAuthenticated]

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
                key='access_token', value=str(access_token), httponly=True, secure=False, samesite=None,
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
            permission_classes = [IsAuthenticated & (IsOwnerUser | IsAdminUser)]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        if IsAuthenticated().has_permission(request, self):
            if IsAdminUser().has_permission(request, self):
                queryset = self.get_queryset()
            else:
                queryset = self.get_queryset().get(id=request.user.id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response([], status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return response


class CombatantViewSet(viewsets.ModelViewSet):
    queryset = Combatant.objects.all()
    serializer_class = CombatantSerializer

    def get_permissions(self):
        if self.action in ('create', 'list'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated & (IsOwnerUser | IsAdminUser)]
        return [permission() for permission in permission_classes]
    
    #Feito com o chatGPT
    def perform_create(self, serializer):
        # Automatically associate the authenticated user
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        if IsAuthenticated().has_permission(request, self):
            if IsAdminUser().has_permission(request, self):
                queryset = self.get_queryset()
            else:
                queryset = self.get_queryset().filter(user=request.user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        if self.action in ('create', 'list'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated & (IsOwnerUser | IsAdminUser)]
        return [permission() for permission in permission_classes]
    
    #Feito com o chatGPT
    def perform_create(self, serializer):
        # Automatically associate the authenticated user
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        if IsAuthenticated().has_permission(request, self):
            if IsAdminUser().has_permission(request, self):
                queryset = self.get_queryset()
            else:
                group_ids = (CombatantGroup.objects.filter(combatant__user=request.user)
                             .values_list('group', flat=True).distinct())
                queryset = self.get_queryset().filter(id__in=group_ids)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)


class CombatantGroupViewSet(viewsets.ModelViewSet):
    queryset = CombatantGroup.objects.all()
    serializer_class = CombatantGroupSerializer

    def get_permissions(self):
        if self.action in ('create', 'list'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated & (IsOwnerUser | IsAdminUser)]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        if IsAuthenticated().has_permission(request, self):
            if IsAdminUser().has_permission(request, self):
                queryset = self.get_queryset()
            else:
                queryset = self.get_queryset().filter(combatant__user=request.user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)


class EncounterViewSet(viewsets.ModelViewSet):
    queryset = Encounter.objects.all()
    serializer_class = EncounterSerializer

    def get_permissions(self):
        if self.action in ('create', 'list'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated & (IsOwnerUser | IsAdminUser)]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        if IsAuthenticated().has_permission(request, self):
            if IsAdminUser().has_permission(request, self):
                queryset = self.get_queryset()
            else:
                queryset = self.get_queryset().filter(combatant__user=request.user)  # TODO MUDAR
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)


class EnemyEncounterViewSet(viewsets.ModelViewSet):
    queryset = EnemyEncounter.objects.all()
    serializer_class = EnemyEncounterSerializer

    def get_permissions(self):
        if self.action in ('create', 'list'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated & (IsOwnerUser | IsAdminUser)]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        if IsAuthenticated().has_permission(request, self):
            if IsAdminUser().has_permission(request, self):
                queryset = self.get_queryset()
            else:
                queryset = self.get_queryset().filter(combatant__user=request.user)  # TODO MUDAR
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)


class AmbientViewSet(viewsets.ModelViewSet):
    queryset = Ambient.objects.all()
    serializer_class = AmbientSerializer

    def get_permissions(self):
        if self.action in ('create', 'list'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated & (IsOwnerUser | IsAdminUser)]
        return [permission() for permission in permission_classes]
    
    #Feito com o chatGPT
    def perform_create(self, serializer):
        # Automatically associate the authenticated user
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        if IsAuthenticated().has_permission(request, self):
            if IsAdminUser().has_permission(request, self):
                queryset = self.get_queryset()
            else:
                queryset = self.get_queryset().filter(combatant__user=request.user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
