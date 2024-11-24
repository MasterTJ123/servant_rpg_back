from .models import Usuario
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

class CustomAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        return True

    def authenticate(self, request, **credentials):
        email = credentials.get('email')
        senha = credentials.get('senha')

        try:
            usuario = Usuario.objects.get(email=email)

            if check_password(senha, usuario.senha):
                return usuario
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None