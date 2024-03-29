# Generated by Django 4.2.9 on 2024-03-10 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_remove_post_likes_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='following',
            new_name='followed',
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('follower', 'followed')},
        ),
    ]
