from django.db import models
from django.forms import ValidationError

class RoomType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

class Room(models.Model):
    code = models.CharField(max_length=255, unique=True)
    building = models.CharField(max_length=255)
    reqAccessCard = models.BooleanField()
    maxOccupancy = models.IntegerField()
    roomType = models.ForeignKey(RoomType, null=False, blank=False, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.code

class GradeMode(models.Model):
    name = models.CharField(max_length=255, unique=True)
    isCreditCounted = models.BooleanField()
    def __str__(self) -> str:
        return self.name

class FacultyType(models.Model):
    FACULTY_TYPE_CHOICES = [
        ("Full Time", "Full Time"),
        ("Contract", "Contract")
    ]
    FacType = models.CharField(max_length=255, choices=FACULTY_TYPE_CHOICES)
    isTenureBased = models.BooleanField()
    employmentStatus = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.FacType

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    txstProfile = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, null=False, blank=False, on_delete=models.PROTECT)
    facultyType = models.ForeignKey(FacultyType, null=False, blank=False, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name

class Course(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    credits = models.IntegerField()
    hasLab = models.BooleanField()
    isLabRequired = models.BooleanField()
    courseCredits = models.IntegerField()
    labCredits = models.IntegerField()
    gradeMode = models.ForeignKey(GradeMode, null=False, blank=False, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, null=False, blank=False, on_delete=models.PROTECT)
    courseAttributes = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class CoursePrerequisite(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='course_prerequisites')
    prerequisite = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='is_prerequisite_for')
    Type = models.CharField(max_length=255, default="Mandetory")
    Condition = models.CharField(max_length=255)

    class Meta:
        unique_together = (('course', 'prerequisite'),)
    
    def __str__(self) -> str:
        return self.course.name

    def clean(self):
        if self.course_id == self.prerequisite_id:
            raise ValidationError("A course cannot be a prerequisite of itself.")
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class CourseCorequisite(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='course_corequisites')
    corequisite = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='is_corequisite_for')
    Type = models.CharField(max_length=255, default="Mandetory")
    Condition = models.CharField(max_length=255, default="grade of 'C' or better")

    class Meta:
        unique_together = (('course', 'corequisite'),)

    def __str__(self) -> str:
        return self.course.name

    def clean(self):
        if self.course_id == self.prerequisite_id:
            raise ValidationError("A course cannot be a corequisite of itself.")
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
