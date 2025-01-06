# models.py

from django.db import models

class Person(models.Model):
    person_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    roll_no = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    validity = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='in')
    count = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

class ImageInfo(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    largest_face = models.ImageField(upload_to='largest_faces/')
    latecomers = models.IntegerField(default=0)
    outside_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)


'''
# attendance_app/models.py
from django.db import models

class Person(models.Model):
    person_id = models.CharField(max_length=255, unique=True)

class Attendance(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    file_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    roll_no = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    validity = models.CharField(max_length=255)
    largest_face = models.CharField(max_length=255)
    in_out_status = models.CharField(max_length=10)
    count = models.IntegerField()
    latecomers = models.IntegerField()
    outside_count = models.IntegerField()
'''