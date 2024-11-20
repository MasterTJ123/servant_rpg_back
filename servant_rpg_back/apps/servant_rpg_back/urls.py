from django.urls import path
from .views import cadastrar_usuario, deletar_usuario, atualizar_usuario, visualizar_usuario

urlpatterns = [
    path('cadastrarusuario', cadastrar_usuario, name='cadastrar_usuario'),
    path('visualizarusuario', visualizar_usuario, name='visualizar_usuario'),
    path('atualizarusuario', atualizar_usuario, name='atualizar_usuario'),
    path('deletarusuario', deletar_usuario, name='deletar_usuario'),
]
