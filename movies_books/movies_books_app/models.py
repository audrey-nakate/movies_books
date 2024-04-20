from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    '''model for the different genres of books and movies'''
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    '''Model for books stored in the library'''
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='covers/', default='default_book_cover_image.png')

    def __str__(self):
        return self.title
    
class Review(models.Model):
    '''Model for reviews made by users'''
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.id} - Rating: {self.rating}"
    
class Profile(models.Model):
    '''Model for the user profile page'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(default='default_user_profile_image.png', upload_to='profile_images/')
    bio = models.TextField(max_length=1000, blank = True)

    def __str__(self):
        return self.user.username
