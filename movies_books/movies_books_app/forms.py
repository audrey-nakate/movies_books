from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignupForm(UserCreationForm):
    ''''Form for the user signup form'''
    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']

        username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Input your username',
    })) 

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder' : 'Input your email address',
    })) 

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Input your password',
    }))   

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Repeat your password',
    }))


class LoginForm(forms.Form):
    ''''Form for the user login form'''
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Input your username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Input your password',
    }))


class ReviewForm(forms.Form):
    '''Form to add reviews under books'''
    rating = forms.IntegerField(min_value=1, max_value=5)
    comment = forms.CharField(widget=forms.Textarea)

class UpdateProfileForm(forms.ModelForm):
    ''''Form for users to update their profile page information'''
    profile_image = forms.ImageField(widget=forms.FileInput)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 8, 'placeholder': 'Tell the community about yourself.'}))

    class Meta:
        model = Profile
        fields = ['profile_image', 'bio']

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_image'].widget.attrs['accept'] = 'image/*' # to ensure that only image files are accepted.

class CreateChatRoomForm(forms.ModelForm):
    ''''Form for users to update their profile page information'''
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name your chatroom'}))
    room_image = forms.ImageField(widget=forms.FileInput)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 8, 'placeholder': 'Tell the community about yourself.'}))

    class Meta:
        model = Profile
        fields = ['name', 'room_image', 'description']

    def __init__(self, *args, **kwargs):
        super(CreateChatRoomForm, self).__init__(*args, **kwargs)
        self.fields['room_image'].widget.attrs['accept'] = 'image/*'