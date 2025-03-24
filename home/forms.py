from django import forms
from django.contrib.auth.models import User
from django.db.models import F  

from home import models

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
from .models import Room, Staff

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
        


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'room_type', 'room_number', 'date_exit', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'room_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose a Room Type'}),
            'room_number': forms.Select(attrs={'class': 'form-control'}),
            'date_exit': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }

    # Filtering available rooms based on selected room type
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields['room_number'].queryset = Room.objects.none()

        if 'room_type' in self.data:
            room_type = self.data.get('room_type')
            self.fields['room_number'].queryset = Room.objects.filter(
                room_type=room_type, occupied__lt=F('capacity')
            )