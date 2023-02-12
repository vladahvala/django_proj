from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}))
    about = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows': 4}))
    class Meta:
        model = Profile
        fields = ['avatar', 'about']