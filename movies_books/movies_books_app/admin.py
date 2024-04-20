from django.contrib import admin
from .models import Book, Genre, Review, Profile

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('genre',)
    search_fields = ('title', 'author')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Review)

admin.site.register(Profile)