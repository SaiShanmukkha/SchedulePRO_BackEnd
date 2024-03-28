from django.contrib import admin
from . import models

class RoomAdmin(admin.ModelAdmin):
    fields = ["code", "building", "reqAccessCard", "maxOccupancy", "roomType"]

# Register your models here.
admin.site.register(models.RoomType)
admin.site.register(models.GradeMode)
admin.site.register(models.Department)
admin.site.register(models.FacultyType)
admin.site.register(models.Room)
admin.site.register(models.Faculty)
admin.site.register(models.Course)
admin.site.register(models.CoursePrerequisite)
admin.site.register(models.CourseCorequisite)
