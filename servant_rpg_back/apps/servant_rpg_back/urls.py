from django.urls import path
from .views import cadastrar_usuario, deletar_usuario, atualizar_usuario, visualizar_usuario, obter_token
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # JWT
    path('api/token', obter_token, name='obter_token'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # Usuario
    path('cadastrarusuario', cadastrar_usuario, name='cadastrar_usuario'),
    path('visualizarusuario', visualizar_usuario, name='visualizar_usuario'),
    path('atualizarusuario', atualizar_usuario, name='atualizar_usuario'),
    path('deletarusuario', deletar_usuario, name='deletar_usuario'),
]
