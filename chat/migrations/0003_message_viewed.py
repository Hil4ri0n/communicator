# Generated by Django 5.0.2 on 2024-04-22 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_chatroom_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
