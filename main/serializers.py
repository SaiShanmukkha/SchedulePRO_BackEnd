from rest_framework import serializers
from .models import Faculty, Course


class FacultySerealizer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.name")
    facultyType = serializers.CharField(source="facultyType.FacType")
    class Meta:
        model = Faculty
        fields = "__all__"


class CourseSerealizer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.name")
    # gradeMode = serializers.CharField(source="gradeMode.name")
    class Meta:
        model = Course
        # fields = "__all__"
        exclude = ["description", "courseAttributes", "gradeMode"]