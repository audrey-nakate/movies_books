# Generated by Django 4.2.7 on 2024-04-21 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies_books_app', '0009_chatroom_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='book',
        ),
    ]
