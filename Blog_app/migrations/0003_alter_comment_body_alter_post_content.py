# Generated by Django 4.2.6 on 2023-10-31 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_app', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(max_length=350),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=350),
        ),
    ]