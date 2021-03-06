# Generated by Django 3.1 on 2020-08-25 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0013_auto_20200825_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile-pictures'),
        ),
        migrations.AlterUniqueTogether(
            name='profile',
            unique_together=set(),
        ),
    ]
