# Generated by Django 4.1.3 on 2022-12-21 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_slug',
            field=models.CharField(default='default_post', max_length=80),
        ),
    ]
