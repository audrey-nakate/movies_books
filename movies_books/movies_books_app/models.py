from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    cover_image = models.ImageField(upload_to='book_covers/', default='images/default_book_cover_image.png')

    def __str__(self):
        return self.title
    
class Movie(models.Model):
    '''Model for movies stored in the library'''
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/', default='images/default_book_cover_image.png')

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
    profile_image = models.ImageField(default='images/default_user_profile_image.png', upload_to='profile_images/')
    bio = models.TextField(max_length=1000, blank = True)

    def __str__(self):
        return self.user.username

class ChatRoom(models.Model):
    '''Model for the chatrooms that will be used to discuss books'''
    # book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='book_chatroom') will include this another time, to allow a chatroom to be associated with a book
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    room_image = models.ImageField(default='images/default_room_image.png', upload_to='room_images/', null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_chatroom')
    created_at = models.DateTimeField(default=timezone.now)
    users = models.ManyToManyField(User, related_name='chatrooms')

    # def __str__(self):
    #     return f"ChatRoom for {self.book.title}"
    
class Message(models.Model):
    '''Model for the messages that will be send in the different chatrooms'''
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)