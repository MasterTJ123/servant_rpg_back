from .models import Usuario
from rest_framework.decorators import authentication_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([AllowAny])
def obter_token(request):
    email = request.data.get('email')
    senha = request.data.get('senha')

    if not email or not senha:
        return Response(
            {"erro": "Os campos 'email' e 'senha' são obrigatórios!"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request=request, email=email, senha=senha)
    if user is None:
        return Response(
            {"erro": "Credenciais inválidas ou usuário inexistente!"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)

    return Response({
        "refresh": str(refresh),
        "access": str(access),
        "nome": user.nome,
        "email": user.email
    })


@api_view(['POST'])
@permission_classes([AllowAny])
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
            status=status.HTTP_200_OK
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

        # Gerar novo token JWT
        refresh = RefreshToken.for_user(usuario)
        novo_token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return Response(
            {
                "mensagem": "Usuário atualizado com sucesso!",
                "novo_token": novo_token
            },
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
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"erro": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
