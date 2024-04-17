from rest_framework import serializers
from main.serializers import CustomFacultySerializer
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
    faculty = CustomFacultySerializer(read_only=True)
    start_time = serializers.TimeField(format='%H:%M')
    end_time = serializers.TimeField(format='%H:%M')
    class Meta:
        model = ScheduleSection
        fields = '__all__' 

class ScheduleSectionCRUDSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(format='%H:%M')
    end_time = serializers.TimeField(format='%H:%M')
    class Meta:
        model = ScheduleSection
        exclude = ["lastUpdated", "createdAt"]


# class ScheduleSectionTimeSerializer(serializers.ModelSerializer):
#     start_time = serializers.TimeField(format='%H:%M')
#     end_time = serializers.TimeField(format='%H:%M')
#     class Meta:
#         model = ScheduleSectionTime
#         fields = '__all__'


# class CUSTOMScheduleFacultySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ScheduleFaculty
#         fields = ['id', 'name']

# class CUSTOMScheduleSectionTimeSerializer(serializers.ModelSerializer):
#     faculty_details = CUSTOMScheduleFacultySerializer(source='schedule_section.faculty', read_only=True)
#     start_time = serializers.TimeField(format='%H:%M')
#     end_time = serializers.TimeField(format='%H:%M')

#     class Meta:
#         model = ScheduleSectionTime
#         fields = ['id', 'schedule', 'schedule_course', 'schedule_section', 'day', 'start_time', 'end_time', 'faculty_details']
