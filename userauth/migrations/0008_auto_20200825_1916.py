# Generated by Django 3.1 on 2020-08-25 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0007_auto_20200825_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
