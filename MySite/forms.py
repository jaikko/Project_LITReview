from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import User,Ticket, Review




class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': "Nom d'utlisateur"}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, required=True)
    rePassword = forms.CharField(max_length=32, widget=forms.PasswordInput, required=True)
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['rePassword'].widget.attrs['placeholder'] = 'Mot de passe'
        self.fields['password'].widget.attrs['placeholder'] = 'Retapez mot de passe'
       
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).count():raise forms.ValidationError("Ce nom d'utilisateur est déjà utilisé")
        return username
 

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'password': forms.PasswordInput(),
            'username': forms.TextInput() 
        }
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Nom d'utlisateur"
        self.fields['password'].widget.attrs['placeholder'] = 'Mot de passe'
    
    
class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description','image')
    

class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description','image')
        widgets = {
            'image': widgets.FileInput(),
        }
    
    
class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline','body']


class FollowUser(forms.Form):
    
    follow = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': "Tapez le nom d'utilisateur "}))
    
