# Generated by Django 4.2.7 on 2024-04-03 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_books_app', '0003_remove_book_genre_alter_genre_name_book_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]