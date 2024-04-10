from rest_framework import serializers
from .models import Schedule, ScheduleCourse, ScheduleFaculty, ScheduleSection

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
    class Meta:
        model = ScheduleSection
        fields = '__all__'
