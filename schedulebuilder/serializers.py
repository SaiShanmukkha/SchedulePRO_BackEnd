from rest_framework import serializers

from main.serializers import CustomFacultySerializer
from .models import Schedule, ScheduleCourse, ScheduleFaculty, ScheduleSection, ScheduleSectionTime

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"

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

    class Meta:
        model = ScheduleSection
        fields = '__all__' 



class ScheduleSectionTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleSectionTime
        fields = '__all__'