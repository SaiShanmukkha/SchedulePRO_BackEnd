from rest_framework import serializers
from .models import Faculty, Course, CourseCorequisite


class FacultySerializer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.name")
    facultyType = serializers.CharField(source="facultyType.FacType")
    class Meta:
        model = Faculty
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.name")
    # gradeMode = serializers.CharField(source="gradeMode.name")
    class Meta:
        model = Course
        # fields = "__all__"
        exclude = ["description", "courseAttributes", "gradeMode"]


class CourseCorequisiteSerializer(serializers.ModelSerializer):
    corequisite = CourseSerializer(read_only=True)

    class Meta:
        model = CourseCorequisite
        exclude = ["Condition"]