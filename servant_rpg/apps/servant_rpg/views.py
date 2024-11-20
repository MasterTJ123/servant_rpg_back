from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Usuario


@api_view(['POST'])
def cadastrar_usuario(request):
    try:
        email = request.data.get('email')
        nome = request.data.get('nome')
        senha = request.data.get('senha')

        if not email or not nome or not senha:
            return Response(
                {"erro": "Campos 'email', 'nome' e 'senha' são obrigatórios!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Usuario.objects.create_user(email=email, nome=nome, senha=senha)

        return Response(
            {"mensagem": "Usuário criado com sucesso!"},
            status=status.HTTP_400_BAD_REQUEST
        )
    except ValidationError as e:
        return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"erro": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def visualizar_usuario(request):
    try:
        usuario = request.user

        context = {
            'nome': usuario.nome,
            'email': usuario.email,
        }

        return Response(
            context,
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"erro": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def atualizar_usuario(request):
    try:
        usuario = request.user

        nome = request.data.get('nome')
        email = request.data.get('email')
        senha = request.data.get('senha')

        if nome:
            usuario.nome = nome
        if email:
            usuario.email = email
        if senha:
            usuario.set_password(senha)

        usuario.save()

        return Response(
            {"mensagem": "Usuário atualizado com sucesso!"},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"erro": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def deletar_usuario(request):
    try:
        usuario = request.user
        usuario.delete()

        return Response(
            {"mensagem": "Usuário deletado com sucesso!"},
            status=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        return Response(
            {"erro": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
