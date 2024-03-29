# Generated by Django 4.2.7 on 2024-01-15 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0016_remove_postmodel_like_dislike_postmodel_dislike_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postmodel',
            name='dislike',
        ),
        migrations.RemoveField(
            model_name='postmodel',
            name='post_image',
        ),
        migrations.CreateModel(
            name='LikeDislikeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField(default=0)),
                ('like', models.IntegerField(blank=True, default=0, null=True)),
                ('dislike', models.IntegerField(blank=True, default=0, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likeuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='postmodel',
            name='like_unlike',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.likedislikemodel'),
        ),
    ]
