# Generated by Django 4.2.6 on 2023-11-10 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_app', '0015_alter_post_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='author',
            new_name='author_id',
        ),
    ]
