from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import SignupForm, LoginForm, UpdateProfileForm, CreateChatRoomForm
from django.contrib.auth.models import User
from .models import Book, Genre, Review, ChatRoom, Message

# view for the website signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

# view for the website login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('books_home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

# view for the website logout page
def user_logout(request):
    logout(request)
    return redirect('books_home')

# view that will list all the books stored in the database
# will also be the home page or landing page of the site
def book_list(request):
    book_list = Book.objects.all()
    return render(request, 'books_home.html', {'book_list': book_list})

# view that handles showing the details of an indivudual book
@login_required(login_url='login')
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book_detail.html', {'book': book})

#view for the search function on the home page
def search_results(request):
    query = request.GET.get('query')
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'search_results.html', {'books': books})

#view to handle user review submissions
@require_POST
def submit_review(request, book_id):
    # Extract the review data from the POST request
    import json
    data = json.loads(request.body.decode("utf-8"))
    rating = data.get('rating')
    comment = data.get('comment')

    book = get_object_or_404(Book, pk=book_id) #book_id is used in the submit_review url to associate a review with a book
    # Create a new Review object and save it to the database
    review = Review.objects.create(book=book, rating=rating, comment=comment)
    # Return a JSON response with the newly created review data
    return JsonResponse({'id': review.id, 'rating': review.rating, 'comment': review.comment})

# view that handles updates made to the profile page of the user
@login_required(login_url='login')
def update_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        profile = request.user.profile
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='view_profile', username=user.username)
    else:
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'update_profile.html', {'form': profile_form, 'user':user})

# view that handles the profile page of the user
@login_required(login_url='login')
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    chatrooms = ChatRoom.objects.filter(users=user)
    return render(request, "view_profile.html", {'user':user, 'profile':profile, 'chatrooms': chatrooms})

@login_required(login_url='login')
def create_chatroom(request):
    if request.method == 'POST':
        create_chatroom_form = CreateChatRoomForm(request.POST, request.FILES)

        if create_chatroom_form.is_valid():
            name = request.POST.get('name')
            room_image = request.POST.get('room_image')
            description = request.POST.get('description')
            chatroom = ChatRoom.objects.create(name=name, room_image=room_image, description=description, created_by=request.user)
            return redirect(to='view_chatroom', chatroom_id=chatroom.id)
    else:
        create_chatroom_form = CreateChatRoomForm()
        
    return render(request, 'create_chatroom.html', {'form': create_chatroom_form})

@login_required(login_url='login')
def view_chatroom(request, chatroom_id):
    chatroom = ChatRoom.objects.get(id=chatroom_id)
    messages = Message.objects.filter(chatroom=chatroom)
    return render(request, 'view_chatroom.html', {'chatroom': chatroom, 'messages': messages})

@login_required(login_url='login')
def send_message(request, chatroom_id):
    if request.method == 'POST':
        chatroom = ChatRoom.objects.get(id=chatroom_id)
        content = request.POST.get('content')
        Message.objects.create(chatroom=chatroom, sender=request.user, content=content)
        return redirect('view_chatroom', chatroom_id=chatroom_id)
    

# view that will list all the chatrooms that have been created
def chatroom_list(request):
    chatroom_list = ChatRoom.objects.all()
    return render(request, 'chatroom_list.html', {'chatroom_list': chatroom_list})

# view that filters books by selected genre
# def genre_books(request, genre_name):
#     genre = get_object_or_404(Genre, name=genre_name)
#     books = Book.objects.filter(genre=genre)
#     return render(request, 'books/genre_books.html', {'genre': genre, 'books': books})