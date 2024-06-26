# Generated by Django 5.0.5 on 2024-06-01 14:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=90, unique=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('contact', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=128)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('role', models.CharField(choices=[('user', 'User'), ('admin', 'Admin')], default='user', max_length=5)),
            ],
            options={
                'db_table': 'tblemployee',
            },
        ),
        migrations.CreateModel(
            name='Courrier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expediteur', models.CharField(max_length=100)),
                ('destinataire', models.CharField(max_length=100)),
                ('type_courrier', models.CharField(max_length=100)),
                ('date_reception', models.DateField()),
                ('reference_courrier', models.CharField(max_length=100)),
                ('est_recu', models.BooleanField(default=False)),
                ('statut', models.CharField(default='en cours', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90)),
                ('email', models.EmailField(max_length=254)),
                ('contact', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'tblvisitor',
            },
        ),
        migrations.CreateModel(
            name='Visite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objet', models.CharField(max_length=90)),
                ('date_debut', models.DateTimeField()),
                ('date_fin', models.DateTimeField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('visiteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.visitor')),
            ],
            options={
                'db_table': 'myapp_visite',
            },
        ),
    ]
