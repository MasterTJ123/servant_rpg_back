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


class Combatant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             null=True, blank=True)  # Set to null if include_generative is True
    name = models.CharField(max_length=100, null=False, blank=False)
    level = models.PositiveIntegerField(null=False, blank=False)
    choosen_class = models.CharField(max_length=100, null=False, blank=False)
    family = models.CharField(max_length=100, null=False, blank=False)
    life = models.PositiveIntegerField(null=False, blank=False)
    armor = models.PositiveIntegerField(null=False, blank=False)
    initiative = models.PositiveIntegerField(null=False, blank=False)
    spell_slots = models.TextField(null=False, blank=False)
    weapon_proficiency = models.PositiveIntegerField(null=False, blank=False)
    magic_proficiency = models.PositiveIntegerField(null=False, blank=False)
    size = models.PositiveIntegerField(null=False, blank=False)
    traits = models.TextField(null=False, blank=False)
    include_generative = models.BooleanField(null=False, blank=False)


class Group(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    campaign = models.CharField(max_length=100, null=False, blank=False)


class CombatantGroup(models.Model):
    combatant = models.ForeignKey(Combatant, on_delete=models.CASCADE, null=False, blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
    group_entry = models.DateField(null=False, blank=False)
    group_exit = models.DateField(null=False, blank=False)


class Encounter(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
    start = models.DateField(null=False, blank=False)
    end = models.DateField(null=False, blank=False)
    turn_history = models.TextField(null=False, blank=False)


class EnemyEncounter(models.Model):
    combatant = models.ForeignKey(Combatant, on_delete=models.CASCADE, null=False, blank=False)
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, null=False, blank=False)


class Ambient(models.Model):
    combatant = models.ForeignKey(Combatant, on_delete=models.CASCADE, null=False, blank=False)
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    families = models.TextField(null=False, blank=False)
    characteristics = models.TextField(null=False, blank=False)
