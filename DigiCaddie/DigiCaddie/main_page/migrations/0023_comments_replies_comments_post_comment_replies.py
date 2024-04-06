# Generated by Django 4.2.7 on 2024-03-23 23:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_page', '0022_alter_userpost_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='comments_replies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('likes_comment', models.ManyToManyField(blank=True, related_name='comment_com_like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comments_post',
            name='comment_replies',
            field=models.ManyToManyField(blank=True, related_name='comment_replies', to='main_page.comments_replies'),
        ),
    ]
