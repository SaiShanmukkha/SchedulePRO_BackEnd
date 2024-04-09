from rest_framework import serializers
from .models import Schedule, ScheduleCourse, ScheduleFaculty, ScheduleSection

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


class ScheduleCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleCourse
        fields = '__all__'

class ScheduleFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleFaculty
        fields = '__all__'

class ScheduleSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleSection
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    courses = ScheduleCourseSerializer(many=True, read_only=True, source='schedulecourse_set')
    faculties = ScheduleFacultySerializer(many=True, read_only=True, source='schedulefaculty_set')

    class Meta:
        model = Schedule
        fields = ['id', 'name', 'courses', 'faculties', 'semester', 'status', 'lastUpdated', 'createdAt', 'slug']