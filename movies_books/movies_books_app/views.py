from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm
from .models import Book, Genre

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
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

# view for the website logout page
def user_logout(request):
    logout(request)
    return redirect('home')

# view that will list all the books stored in the database
# will also be the home page or landing page of the site
def book_list(request):
    book_list = Book.objects.all()
    return render(request, 'home.html', {'book_list': book_list})

# view that handles showing the details of an indivudual book
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book_detail.html', {'book': book})

#view for the search function on the home page
def search_results(request):
    query = request.GET.get('query')
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'books/search_results.html', {'books': books})

# view that filters books by selected genre
# def genre_books(request, genre_name):
#     genre = get_object_or_404(Genre, name=genre_name)
#     books = Book.objects.filter(genre=genre)
#     return render(request, 'books/genre_books.html', {'genre': genre, 'books': books})