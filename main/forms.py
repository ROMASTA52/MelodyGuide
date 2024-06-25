from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, LikeDislike
from .models import Comment

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'age', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class LikeDislikeForm(forms.ModelForm):
    content_type = forms.CharField()
    object_id = forms.IntegerField()
    
    class Meta:
        model = LikeDislike
        fields = ['vote']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']