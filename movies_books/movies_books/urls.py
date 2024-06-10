"""
URL configuration for movies_books project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from movies_books_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  views.book_list, name='books_home'),
    path('search/', views.search_results, name='search_results'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('book_detail/<book_id>/',views.book_detail,name ='book_detail'),
    path('books/<int:book_id>/submit_review/', views.submit_review, name='submit_review'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('profile/<str:username>/update/', views.update_profile, name='update_profile'),
    path('create_chatroom/', views.create_chatroom, name='create_chatroom'),
    path('book_discussion/<int:chatroom_id>/', views.view_chatroom, name='view_chatroom'),
    path('chatroom_list/', views.chatroom_list, name='chatroom_list'),
    path('join_chatroom/<int:chatroom_id>/', views.join_chatroom, name='join_chatroom'),
    path('chatroom/<int:chatroom_id>/exit/', views.exit_chatroom, name='exit_chatroom'),
    path('chatroom_search/', views.chatroom_search_results, name='chatroom_search_results'),
    path('chatroom/<int:chatroom_id>/delete/', views.delete_chatroom, name='delete_chatroom'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

