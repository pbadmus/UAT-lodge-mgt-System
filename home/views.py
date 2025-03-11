from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RoomForm
from django.http import JsonResponse
from django.db.models import Sum

def admin_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Get user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials.")
            return redirect('admin-login')

        # Authenticate user
        user = authenticate(request, username=user.username, password=password)

        if user is not None:   #and user.is_staff, i want to check this with against the school db
            
            if not user.is_staff:
                user.is_staff = True
                user.save()
                 
            login(request, user)
            return redirect('admin-dashboard')  
        else:
            messages.error(request, "Invalid credentials or unauthorized access.")

    return render(request, 'admin-login.html')

def home(request):
    return render(request, 'home.html')


def dashboard(request):
    room = Room.objects.all()
    room_count = room.count()
    total_capacity = room.aggregate(Sum("capacity"))["capacity__sum"] or 0
    return render(request,
                  'admin-dashboard.html', 
                  {"room_count": room_count, 
                   "total_capacity": total_capacity}
                  )

def rooms(request):
    room = Room.objects.all()
    return render(request, 'admin-rooms.html', {'rooms': room})
    

def admin_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('admin-login')

def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('room-list'))  # Redirect to room list page

    else:
        form = RoomForm()

    return render(request, 'new_room.html', {'form': form})

from .models import Room
def room_list(request):
    room = Room.objects.all()
    form = RoomForm()
    return render(request, 'admin-rooms.html', {'rooms': room, 'form': form})


def staff_room(request):
    return render(request, 'staff-room.html')