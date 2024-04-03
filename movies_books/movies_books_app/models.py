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
    
class Review(models.Model):
    '''Model for reviews made by users'''
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.id} - Rating: {self.rating}"
    
