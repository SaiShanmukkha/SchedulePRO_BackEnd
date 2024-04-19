from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from main.models import Course, Faculty, Room, Department, Semester
from datetime import datetime


class Schedule(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
        ('Trashed', 'Trashed'),
    ]
    name = models.CharField(max_length=255, unique=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=255, default='Draft', choices=STATUS_CHOICES)
    lastUpdated = models.DateTimeField(auto_now=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    def __str__(self) -> str:
        return self.name

def pre_save_my_model_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name+ datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

pre_save.connect(pre_save_my_model_receiver, sender=Schedule)



class ScheduleCourse(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(max_length=255, null=False, blank=False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    number_of_labs = models.IntegerField(default=0)
    number_of_sections = models.IntegerField(default=1)
    course_credit = models.IntegerField(null=False, blank=False)
    lab_credit = models.IntegerField(null=False, blank=False)
    lastUpdated = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.code + " " + self.course.name

    
class ScheduleFaculty(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.schedule.name + " " + self.name

class ScheduleRoom(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    schdule_course = models.ForeignKey(ScheduleCourse, on_delete=models.CASCADE)
    lastUpdated = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.schedule.name + " " + self.room.code
    

class ScheduleSection(models.Model):
    TYPE_CHOICES = [
        ('Class', 'Class'),
        ('Lab', 'Lab'),
    ]
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    schedule_course = models.ForeignKey(ScheduleCourse, on_delete=models.CASCADE)
    faculty = models.ForeignKey(ScheduleFaculty, on_delete=models.CASCADE, null=True, blank=True)
    sectionType = models.CharField(max_length=255, default='Class', choices=TYPE_CHOICES)
    section_name = models.CharField(max_length=255)
    lastUpdated = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    day = models.CharField(max_length=5, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.schedule_course.code + " " + self.section_name

    class Meta:
        unique_together = ['schedule_course', 'section_name', 'sectionType', 'day', 'start_time', 'end_time']

