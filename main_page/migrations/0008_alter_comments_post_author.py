# Generated by Django 4.2.7 on 2024-01-05 03:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_page', '0007_comments_post_userpost_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments_post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
