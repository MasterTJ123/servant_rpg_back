from .erros import CampoAusente, EmailJaCadastrado, CredenciaisInvalidas
from .models import Usuario
from django.contrib.auth import authenticate
from django.db import OperationalError, IntegrityError
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([AllowAny])
def obter_token(request):
    try:
        email = request.data.get('email')
        senha = request.data.get('senha')

        # Verifica se todos os campos estão presentes
        if not email or not senha:
            raise CampoAusente("Erro! Todos os campos são obrigatórios!")

        user = authenticate(request=request, email=email, senha=senha)

        # Verifica se as credenciais estão corretas e se o usuário existe
        if user is None:
            raise CredenciaisInvalidas("Erro! Credenciais inválidas ou usuário inexistente!")

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({
            "refresh": str(refresh),
            "access": str(access),
            "nome": user.nome,
            "email": user.email
        }, status=status.HTTP_200_OK)
    except CampoAusente as e:
        return Response({"erro": e.mensagem}, status=status.HTTP_400_BAD_REQUEST)
    except CredenciaisInvalidas as e:
        return Response({"erro": e.mensagem}, status=status.HTTP_401_UNAUTHORIZED)
    except OperationalError:
        return Response({"erro": "Erro! Não foi possível acessar o banco de dados!"},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response({"erro": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def cadastrar_usuario(request):
    try:
        email = request.data.get('email')
        nome = request.data.get('nome')
        senha = request.data.get('senha')

        Usuario.objects.create_user(email=email, nome=nome, senha=senha)

        return Response(
            {"mensagem": "Usuário criado com sucesso!"},
            status=status.HTTP_200_OK
        )
    except (CampoAusente, EmailJaCadastrado) as e:
        return Response({"erro": e.mensagem}, status=status.HTTP_400_BAD_REQUEST)
    except OperationalError:
        return Response({"erro": "Erro! Não foi possível acessar o banco de dados!"},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except IntegrityError:
        return Response({"erro": "Erro! Integridade inválida do banco de dados!"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
