from django.db import models

from main.models import Course, Faculty, Room

class Schedule(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
        ('Trashed', 'Trashed'),
    ]
    name = models.CharField(max_length=255)
    semester = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, default='Draft', choices=STATUS_CHOICES)
    lastUpdated = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.name


class ScheduleCourse(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(max_length=255, null=False, blank=False)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    number_of_labs = models.IntegerField(default=0)
    number_of_sections = models.IntegerField(default=1)
    course_credit = models.IntegerField(null=False, blank=False)
    lab_credit = models.IntegerField(null=False, blank=False)
    lastUpdated = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name + "<->" + self.course.name

    
class ScheduleFaculty(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.schedule.name + "<->" + self.name

class ScheduleRoom(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    schdule_course = models.ForeignKey(ScheduleCourse, on_delete=models.CASCADE)
    lastUpdated = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.schedule.name + "<->" + self.room.code
    

class ScheduleSection(models.Model):
    TYPE_CHOICES = [
        ('Class', 'Class'),
        ('Lab', 'Lab'),
    ]
    schedule_course = models.ForeignKey(ScheduleCourse, on_delete=models.CASCADE, related_name='sections')
    faculty = models.ForeignKey(ScheduleFaculty, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(ScheduleRoom, on_delete=models.CASCADE, null=True, blank=True)
    sectionType = models.CharField(max_length=255, default='Class', choices=TYPE_CHOICES)
    section_name = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lastUpdated = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.schedule.name + "<->" + self.section_name

    class Meta:
        unique_together = ['schedule_course', 'section_name', 'sectionType', 'room', 'start_time', 'end_time']
