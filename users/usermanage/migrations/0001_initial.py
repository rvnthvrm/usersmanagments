# Generated by Django 3.1 on 2020-08-13 01:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=40, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(blank=True, max_length=25, verbose_name='Name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Name')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Is SuperUser')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('joined_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Joined at')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
    ]
