from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        validators=[UnicodeUsernameValidator()],
        null=False,
        blank=False
    )
    email = models.EmailField(_("email address"), unique=True, null=False, blank=False)
    password = models.CharField(_("password"), max_length=128, null=False, blank=False)
    first_name = models.CharField(_("first name"), max_length=150, null=False, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, null=False, blank=False)
    USERNAME_FIELD = "email"  # Authentication using an email instead of a username
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]  # Other fields are required by default


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
