# Generated by Django 4.2.7 on 2024-03-24 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_books_app', '0002_genre_book_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(to='movies_books_app.genre'),
        ),
    ]
