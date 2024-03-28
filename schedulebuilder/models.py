from django.db import models

from main.models import Course

# Create your models here.
class Schedule(models.Model):
    name = models.CharField(max_length=255)
    semester = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, default="", choices=["Draft", "Published", "Trashed"])


class ScheduleCourse(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(max_length=255, null=False, blank=False)
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL)
    number_of_labs = models.IntegerField(default=0)
    number_of_sections = models.IntegerField(default=1)
    course_credit = models.IntegerField(null=False, blank=False)
    lab_credit = models.IntegerField(null=False, blank=False)


class ScheduleRoom(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    schdule_course = models.ForeignKey(ScheduleCourse, on_delete=models.CASCADE)
    
    number_of_labs = models.IntegerField(default=0)
    number_of_sections = models.IntegerField(default=1)
    course_credit = models.IntegerField(null=False, blank=False)
    lab_credit = models.IntegerField(null=False, blank=False)
