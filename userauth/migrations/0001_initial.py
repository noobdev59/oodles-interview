# Generated by Django 3.1 on 2020-08-25 18:08

from django.db import migrations, models
import django.db.models.deletion
import phone_field.models
import userauth.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('phone_number', phone_field.models.PhoneField(blank=True, max_length=31, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=255)),
                ('date_of_birth', models.DateTimeField()),
                ('profile_picture', models.ImageField(upload_to=userauth.models.profile_upload_image_handler)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('company_address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company_address', to='utils.address')),
                ('permanent_address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='permanent_address', to='utils.address')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
