from django.contrib import admin
from .models import Student,EntryExitTime
# Register your models here.

@admin.register(Student)
class AdimStudent(admin.ModelAdmin):
    list_display=["id","name"]

@admin.register(EntryExitTime)
class AdminEntryExitTime(admin.ModelAdmin):
    list_display=["stu","EntryTime","ExitTime"]