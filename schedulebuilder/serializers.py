from rest_framework import serializers
from main.models import Department
from main.serializers import CustomFacultySerializer, DepartmentSerializer
from .models import Schedule, ScheduleCourse, ScheduleFaculty, ScheduleSection

class ScheduleSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    class Meta:
        model = Schedule
        fields = "__all__"

class ScheduleCRUDSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), allow_null=True)
    class Meta:
        model = Schedule
        fields = ['id', 'name', 'semester', 'status', 'department', 'createdAt', 'lastUpdated', 'slug']

class ScheduleCourseSerializer(serializers.ModelSerializer):
    credits = serializers.SerializerMethodField()
    class Meta:
        model = ScheduleCourse
        fields = '__all__'
    def get_credits(self, obj):
        return obj.course.credits if obj.course else None

class ScheduleFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleFaculty
        fields = '__all__'

class ScheduleSectionSerializer(serializers.ModelSerializer):
    faculty = CustomFacultySerializer(read_only=True)
    start_time = serializers.TimeField(format='%H:%M')
    end_time = serializers.TimeField(format='%H:%M')
    class Meta:
        model = ScheduleSection
        fields = '__all__' 

class ScheduleSectionCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleSection
        exclude = ["lastUpdated", "createdAt"]
