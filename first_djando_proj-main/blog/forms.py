from django import forms
from django.contrib.auth.models import User
from .models import Profile, Comment
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm): #наслідування
    email = forms.EmailField(max_length=100, help_text="Обов'язкове поле")
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}))
    about = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows': 4}))
    class Meta:
        model = Profile
        fields = ['avatar', 'about']

class AddCommentForm(forms.ModelForm):
    content = forms.CharField(widget= forms.Textarea(attrs={'placeholder':'Comment here...', 'class':'form-control'}))
    #placeholder - текст, який пишеться перед тим як користувач ставить туди курсор
    class Meta:
        model = Comment
        fields = ['content']