# Generated by Django 4.2.7 on 2023-11-20 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0002_alter_userpost_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]