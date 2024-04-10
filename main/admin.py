from django.contrib import admin
from . import models

class RoomAdmin(admin.ModelAdmin):
    list_display  = ["id", "code", "building", "reqAccessCard", "maxOccupancy", "roomType"]

class DepartmentAdmin(admin.ModelAdmin):
    list_display  = ["id", "code", "name"]

class SemesterAdmin(admin.ModelAdmin):
    list_display  = ["id", "name"]

class FacultyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "department", "facultyType"]

class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "name", "department", "credits", "courseCredits", "labCredits", "hasLab", "isLabRequired"]
    list_filter = ["department", "hasLab", "isLabRequired"]

class PrequisiteAdmin(admin.ModelAdmin):
    list_display = ["id", "course", "prerequisite", "Type", "Condition"]

class CorequisiteAdmin(admin.ModelAdmin):
    list_display = ["id", "course", "corequisite", "Type", "Condition"]

# Register your models here.
admin.site.register(models.RoomType)
admin.site.register(models.Semester, SemesterAdmin)
admin.site.register(models.GradeMode)
admin.site.register(models.Department, DepartmentAdmin)
admin.site.register(models.FacultyType)
admin.site.register(models.Room, RoomAdmin)
admin.site.register(models.Faculty, FacultyAdmin)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.CoursePrerequisite, PrequisiteAdmin)
admin.site.register(models.CourseCorequisite, CorequisiteAdmin)
