from .erros import CampoAusente, EmailJaCadastrado, CredenciaisInvalidas
from .models import Usuario
from django.db import OperationalError, IntegrityError
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.servant_rpg_back.backends import JWTCookieAuthentication, NoAuthentication


@api_view(['POST'])
@authentication_classes([NoAuthentication])
@permission_classes([AllowAny])
def access_token(request):
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

        # Resposta
        response = Response({
            "nome": user.nome,
            "email": user.email
        }, status=status.HTTP_200_OK)

        # Cookies
        refresh_aux = RefreshToken.for_user(user)
        access = str(refresh_aux.access_token)
        refresh = str(refresh_aux)

        access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

        response.set_cookie(
            'accessToken',
            access,
            httponly=True,
            secure=False,  # TODO MUDAR PARA TRUE EM PRODUÇÃO
            samesite='Strict',
            max_age=access_token_lifetime
        )

        response.set_cookie(
            'refreshToken',
            refresh,
            httponly=True,
            secure=False,  # TODO MUDAR PARA TRUE EM PRODUÇÃO
            samesite='Strict',
            max_age=refresh_token_lifetime
        )

        return response
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
@authentication_classes([NoAuthentication])
@permission_classes([AllowAny])
def refresh_token(request):
    try:
        refresh_token = request.COOKIES.get('refreshToken')

        if not refresh_token:
            raise AuthenticationFailed("Erro! Refresh token não encontrado nos cookies!")

        response = Response({
            "menssagem": "Tokens renovados com sucesso!"
        }, status=status.HTTP_200_OK)

        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        novo_refresh_token = str(refresh)

        access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

        response.set_cookie(
            'accessToken',
            access_token,
            httponly=True,
            secure=False,  # TODO MUDAR PARA TRUE EM PRODUÇÃO
            samesite='Strict',
            max_age=access_token_lifetime
        )

        response.set_cookie(
            'refreshToken',
            novo_refresh_token,
            httponly=True,
            secure=False,  # TODO MUDAR PARA TRUE EM PRODUÇÃO
            samesite='Strict',
            max_age=refresh_token_lifetime
        )

        return response
    except AuthenticationFailed as e:
        return Response({"erro": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"erro": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([NoAuthentication])
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
    except ValidationError as e:
        erro = e.messages[0]
        if erro.endswith('.'):
            erro = erro[:-1] + '!'
        return Response({"erro": f"Erro! {erro}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"erro": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([JWTCookieAuthentication])
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
@authentication_classes([JWTCookieAuthentication])
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
@authentication_classes([JWTCookieAuthentication])
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
