from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    '''Model for books stored in the library'''
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    
    
