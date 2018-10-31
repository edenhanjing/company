from django.db import models

# Create your models here.

class RoomName(models.Model):
	room_name = models.CharField(max_length=256)
	room_id =  models.CharField(max_length=256)
	read_num = models.IntegerField(default=0)

