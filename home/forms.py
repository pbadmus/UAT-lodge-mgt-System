from django import forms
from django.contrib.auth.models import User

class AdminLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'School Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
    
from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['building', 'room_number', 'room_type', 'capacity']
        widgets = {
            'building': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Building Block (e.g., Block A)'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Room Number (e.g., A101)'}),
            'room_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'standard'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }