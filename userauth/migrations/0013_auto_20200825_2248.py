# Generated by Django 3.1 on 2020-08-25 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0012_auto_20200825_2242'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='profile',
            unique_together={('email', 'phone_number', 'username')},
        ),
    ]
