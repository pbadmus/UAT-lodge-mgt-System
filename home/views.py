from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
import urllib
from .forms import RoomForm, StaffForm
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.db.models import Sum
from .models import Room, Staff
from django.contrib.auth.decorators import login_required


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

        if user is not None:   #and user.is_staff, i want to check this  against the school db
            
            if not user.is_staff:
                user.is_staff = True
                user.save()
                 
            login(request, user)
            return redirect('dashboard')  
        else:
            messages.error(request, "Invalid credentials or unauthorized access.")

    return render(request, 'admin-login.html')

def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    room = Room.objects.all()
    room_count = room.count()
    staff = Staff.objects.all()
    staff_count = staff.count()
    
    # Get the recent lodge and some information about them 
    recent_lodges = Staff.objects.select_related('room_number').order_by('-date_entry')[:5] 
    
    active_lodge = Staff.objects.filter(status='Active').count()
    total_capacity = room.aggregate(Sum("capacity"))["capacity__sum"] or 0
    return render(request,
                  'admin-dashboard.html', 
                  {"room_count": room_count, 
                   "staff_count": staff_count,
                   "total_capacity": total_capacity,
                   "active_lodge": active_lodge,
                   "recent_lodges": recent_lodges})
                  

def rooms(request):
    room = Room.objects.all()
    return render(request, 'admin-rooms.html', {'rooms': room})
    
@login_required
def admin_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('admin-login')

@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('room-list'))  # Redirect to room list page

    else:
        form = RoomForm()

    return render(request, 'new_room.html', {'form': form})

def room_list(request):
    room = Room.objects.all()
    form = RoomForm()
    return render(request, 'admin-rooms.html', {'rooms': room, 'form': form})

# @login_required
def delete_room(request, room_number):
    room_list = get_object_or_404(Room, room_number=room_number)
    if request.method == 'POST':
        room_list.delete()
        return redirect(reverse('admin-room'))  # Redirect to room list page
    return HttpResponseNotAllowed(['POST'])     


@login_required
def edit_room(request, room_number):
    room_list =get_object_or_404(Room, room_number=room_number)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room_list)
        if form.is_valid():
            form.save()
            return redirect('admin-room')
    else:
        form = RoomForm(instance=room_list)
    return render(request, 'new_room.html', {'form': form})
    
    
def staff_room(request):
    staff_list = Staff.objects.all()
    return render(request, 'staff-room.html', {'staff_list': staff_list})

@login_required
def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            
            staff_instance = form.save(commit=False)      # Do nt commit the change yet  
            room = staff_instance.room_number  # Get the staff room number     
            if room:
                if room.occupied < room.capacity:
                    room.occupied = F('occupied') + 1 # Increment occupancy
                    room.save(update_fields = ['occupied'])
                    
                    staff_instance.save()
                    return redirect(reverse('staff-room')) 
                else: 
                    messages.error("This room is already filled")
                
            else:
                messages.error("Please select a room for a staff")# Redirect to staff list page
    else:
        form = StaffForm()
            
    return render(request, 'add_staff.html', {'form': form})
   
   
@login_required 
def delete_staff(request, name):
    staff_list = get_object_or_404(Staff, name=name)
    if request.method == 'POST':
        staff_list.delete()
        return redirect(reverse('staff-room'))  # Redirect to staff list page
    return HttpResponseNotAllowed(['POST'])


@login_required
def edit_staff(request, name):
    try:
        decoded_name = urllib.parse.unquote(name) 
        staff_list = get_object_or_404(Staff, name=decoded_name)
        if request.method == "POST":
            form = StaffForm(request.POST, instance=staff_list)
            if form.is_valid():
                form.save()
                return redirect('staff-room')
            else:
                form = StaffForm(instance=staff_list)
            return render(request, 'add_staff.html', {'form': form})
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

from  django.db.models import F
def available_room(request):
    room_type = request.GET.get('room_type')
    
    if room_type == "Shared":
        rooms = Room.objects.filter(room_type='Shared', occupied__lt=F('capacity'))
    else:
        rooms = Room.objects.filter(room_type='Single', occupied=0)  # Single rooms must be completely empty

    room_list = [{"id": room.id, "room_number": room.room_number} for room in rooms]
    return JsonResponse({"rooms": room_list})


def room_filter(request):  
    query = request.GET.get('q', '').strip()
    if query:
        rooms = Room.objects.filter(room_number__icontains=query) | Room.objects.filter(building__icontains=query)
    else:
        rooms = Room.objects.all()

    return render(request, 'admin-rooms.html', {'rooms': rooms})


def student_filter(request):
    query = request.GET.get('q', '').strip
    if query:
        staffs = Staff.objects.filter(name_icontains=query) 
    else: 
        staffs = Staff.objects.all()
        
    return render(request, 'staff-room.html', {'staff': staffs})