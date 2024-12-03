from .erros import CampoAusente, EmailJaCadastrado
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, senha):
        # Verifica se todos os campos estão presentes
        if not email or not nome or not senha:
            raise CampoAusente("Erro! Todos os campos são obrigatórios!")
        # Verifica se o e-mail já existe
        try:
            Usuario.objects.get(email=email)
            raise EmailJaCadastrado("Erro! O e-mail já está cadastrado!")
        except Usuario.DoesNotExist:
            pass
        # TODO VERIFICAR SE A FORMATAÇÃO DO E-MAIL ESTÁ CORRETA
        # Verifica se a senha é segura
        try:
            usuario_aux = Usuario(email=email, nome=nome, senha=senha)
            validate_password(senha, usuario_aux)
        except ValidationError as e:
            raise ValidationError(e)
        # Cria o usuário
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome)
        user.senha = make_password(senha)
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    senha = models.CharField(max_length=100)

    password = None
    last_login = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'senha']

    objects = UsuarioManager()


class Combatente(models.Model):
    nome = models.CharField(max_length=100)
    nivel = models.PositiveIntegerField()
    classe = models.CharField(max_length=100)
    familia = models.CharField(max_length=100)
    vida = models.PositiveIntegerField()
    armadura = models.PositiveIntegerField()
    iniciativa = models.PositiveIntegerField()
    spell_slots = models.PositiveIntegerField()
    prof_armas = models.PositiveIntegerField()
    prof_magica = models.PositiveIntegerField()
    tamanho = models.PositiveIntegerField()
    traits = models.CharField(max_length=100)
    incluir_gerativo = models.BooleanField()


class Grupo(models.Model):
    nome = models.CharField(max_length=100)


class CombatenteGrupo(models.Model):
    combatente = models.ForeignKey(Combatente, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    entrada_grupo = models.DateField()
    saida_grupo = models.DateField()


class Encontro(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    inicio = models.DateField()
    fim = models.DateField()
    historico_turnos = models.TextField()


class InimigoEncontro(models.Model):
    combatente = models.ForeignKey(Combatente, on_delete=models.CASCADE)
    encontro = models.ForeignKey(Encontro, on_delete=models.CASCADE)
