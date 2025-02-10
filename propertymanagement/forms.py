from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import KYC,Property
class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'  
        })
    )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'  
        })
    )

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']



class KYCForm(forms.ModelForm):
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}))
    class Meta:
        model = KYC
        fields = ['national_id','phone_number']

    
    
class PropertyForm(forms.ModelForm):
    owner_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Owner Name'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    state = forms.ChoiceField(choices=Property._meta.get_field('state').choices, widget=forms.Select(attrs={'class': 'form-control'}))
    property_size = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Property Size'}))
    property_value = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Property Value'}))
    sale_deed = forms.FileField()

    class Meta:
        model = Property
        fields = ['owner_name','address', 'state', 'property_size', 'property_value', 'sale_deed']
