# from django.db import models

# class Building(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name

# class Room(models.Model):
#     ROOM_TYPES = [
#         ('Standard', 'Standard'),
#         ('Premium', 'Premium'),
#     ]

#     STATUS_CHOICES = [
#         ('Active', 'Active'),
#         ('Maintenance', 'Maintenance'),
#     ]

#     building = models.ForeignKey(Building, on_delete=models.CASCADE)
#     room_number = models.CharField(max_length=10, unique=True)  # Added Room Number Field
#     room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
#     capacity = models.IntegerField()
#     students_assigned = models.IntegerField(default=0)
#     status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Active')

#     def occupancy_display(self):
#         return f"{self.students_assigned}/{self.capacity}"

#     def __str__(self):
#         return f"Room {self.room_number} in {self.building.name} - {self.room_type}"


from django.db import models


class Room(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single'),
        ('Shared', 'Shared'),
    ]

    building = models.CharField(max_length=50)  # Manually entered building block
    room_number = models.CharField(max_length=10)  # Manually entered room number
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    capacity = models.IntegerField()
    occupied = models.IntegerField(default=0)  # Tracks current number of students in the room

    def occupancy_display(self):
        return f"{self.occupied}/{self.capacity}"

    def __str__(self):
        return f"{self.building} - Room {self.room_number} ({self.room_type}, {self.occupied}/{self.capacity})"