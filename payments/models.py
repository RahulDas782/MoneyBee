from django.db import models

class Rooms(models.Model):
    Admin = models.CharField(max_length = 100)
    Room_Name = models.CharField(max_length = 100)
    Username = models.CharField(max_length = 100)
    Password = models.CharField(max_length = 100)
    Balance = models.BigIntegerField(default = 5000)  

    def __str__(self):
        return self.Room_Name

class Members(models.Model):
    RoomId = models.ForeignKey('Rooms', on_delete=models.CASCADE)
    Mem_Name = models.CharField(max_length = 100)
    PayId = models.CharField(max_length = 100)
    Balance = models.BigIntegerField(default = 5000)

    def __str__(self):
        return self.Mem_Name
