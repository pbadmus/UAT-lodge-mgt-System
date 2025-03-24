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
    path('rooms/filter/', views.room_filter, name='room-filter'),
    path('add-staff/', views.add_staff, name='add_staff'),
    path('get-available-rooms/', views.available_room, name='get_available_rooms'),
    path('delete-staff/<str:name>/', views.delete_staff, name='delete-staff'),
    path('edit-staff/<str:name>/', views.edit_staff, name='edit-staff'),

]
