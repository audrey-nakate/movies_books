from django.contrib import admin
from .models import Book, Genre, Review, Profile, ChatRoom, Message, Movie

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('genre',)
    search_fields = ('title', 'author')

admin.site.register(Movie)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Review)

admin.site.register(Profile)

admin.site.register(ChatRoom)

admin.site.register(Message)