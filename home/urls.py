from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='welcome'),
    path('admin-login/', views.admin_login, name="admin-login"),
    path('admin-dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.admin_logout, name='admin-logout'),
    path('admin-room/', views.rooms, name="admin-room"),
    path('rooms/', views.rooms, name='room-list'),
    path('add-room/', views.add_room, name='add-room'),
    path('staff-room/', views.staff_room, name='staff-room'),
    path('delete-room/<str:room_number>/', views.delete_room, name='delete-room'),
    path('edit-room/<str:room_number>/', views.edit_room, name='edit-room'),
]
