from rest_framework import serializers
from .models import Department, Faculty, Course, CourseCorequisite, Semester


class FacultySerializer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.name")
    facultyType = serializers.CharField(source="facultyType.FacType")
    class Meta:
        model = Faculty
        fields = "__all__"

class CourseCorequisiteSerializer(serializers.ModelSerializer):
    corequisite_name = serializers.CharField(source='corequisite.name', read_only=True)
    corequisite_code = serializers.CharField(source='corequisite.code', read_only=True)

    class Meta:
        model = CourseCorequisite
        fields = ['id', 'corequisite_name', 'corequisite_code', 'Type']


class CourseSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.name")
    # gradeMode = serializers.CharField(source="gradeMode.name")
    class Meta:
        model = Course
        # fields = "__all__"
        exclude = ["description", "courseAttributes", "gradeMode"]

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'name']

class CourseCorequisiteSerializer(serializers.ModelSerializer):
    corequisite = CourseSerializer(read_only=True)

    class Meta:
        model = CourseCorequisite
        exclude = ["Condition"]

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code']