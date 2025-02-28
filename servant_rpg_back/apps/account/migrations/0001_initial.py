# Generated by Django 5.1.4 on 2024-12-18 21:55

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('turn_history', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('campaign', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Combatant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('level', models.PositiveIntegerField()),
                ('choosen_class', models.CharField(max_length=100)),
                ('family', models.CharField(max_length=100)),
                ('life', models.PositiveIntegerField()),
                ('armor', models.PositiveIntegerField()),
                ('initiative', models.PositiveIntegerField()),
                ('spell_slots', models.TextField()),
                ('weapon_proficiency', models.PositiveIntegerField()),
                ('magic_proficiency', models.PositiveIntegerField()),
                ('size', models.PositiveIntegerField()),
                ('traits', models.TextField()),
                ('include_generative', models.BooleanField()),
                ('user', models.ForeignKey(blank=False, null=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ambient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('families', models.TextField()),
                ('characteristics', models.TextField()),
                ('combatant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.combatant')),
                ('encounter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.encounter')),
            ],
        ),
        migrations.CreateModel(
            name='EnemyEncounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('combatant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.combatant')),
                ('encounter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.encounter')),
            ],
        ),
        migrations.AddField(
            model_name='encounter',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.group'),
        ),
        migrations.CreateModel(
            name='CombatantGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_entry', models.DateField()),
                ('group_exit', models.DateField()),
                ('combatant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.combatant')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.group')),
            ],
        ),
    ]
