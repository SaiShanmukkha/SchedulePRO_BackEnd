from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ScheduleSerializer, ScheduleSectionSerializer, ScheduleCourseSerializer, ScheduleFacultySerializer
from .models import Schedule, ScheduleFaculty, ScheduleCourse, ScheduleSection

# Create your views here.
@api_view(['GET', 'POST'])
def SchedulesView(request):
    if request.method == 'GET':
        schObjs = Schedule.objects.all()
        serealized_data = ScheduleSerializer(schObjs, many=True)
        return Response(serealized_data.data)
    elif request.method == 'POST':
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_BAD_REQUEST)
        


@api_view(['GET', 'PUT'])
def schedule_detail_view(request, pk):
    try:
        schedule = Schedule.objects.get(pk=pk)
    except Schedule.DoesNotExist:
        return Response({'error': 'Schedule not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def schedule_course_view(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                schedule_course = ScheduleCourse.objects.get(pk=pk)
                serializer = ScheduleCourseSerializer(schedule_course)
            except ScheduleCourse.DoesNotExist:
                return Response({'error': 'Schedule Course not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            schedule_courses = ScheduleCourse.objects.all()
            serializer = ScheduleCourseSerializer(schedule_courses, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ScheduleCourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        try:
            schedule_course = ScheduleCourse.objects.get(pk=pk)
        except ScheduleCourse.DoesNotExist:
            return Response({'error': 'Schedule Course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ScheduleCourseSerializer(schedule_course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            schedule_course = ScheduleCourse.objects.get(pk=pk)
            schedule_course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ScheduleCourse.DoesNotExist:
            return Response({'error': 'Schedule Course not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def schedule_faculty_view(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                schedule_faculty = ScheduleFaculty.objects.get(pk=pk)
                serializer = ScheduleFacultySerializer(schedule_faculty)
            except ScheduleFaculty.DoesNotExist:
                return Response({'error': 'Schedule Faculty not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            schedule_faculties = ScheduleFaculty.objects.all()
            serializer = ScheduleFacultySerializer(schedule_faculties, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ScheduleFacultySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            schedule_faculty = ScheduleFaculty.objects.get(pk=pk)
        except ScheduleFaculty.DoesNotExist:
            return Response({'error': 'Schedule Faculty not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ScheduleFacultySerializer(schedule_faculty, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            schedule_faculty = ScheduleFaculty.objects.get(pk=pk)
            schedule_faculty.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ScheduleFaculty.DoesNotExist:
            return Response({'error': 'Schedule Faculty not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PUT'])
def schedule_section_view(request, pk=None):
    if request.method == 'GET':
        if pk:
            # Get a single schedule section
            try:
                schedule_section = ScheduleSection.objects.get(pk=pk)
                serializer = ScheduleSectionSerializer(schedule_section)
            except ScheduleSection.DoesNotExist:
                return Response({'error': 'Schedule Section not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Get all schedule sections
            schedule_sections = ScheduleSection.objects.all()
            serializer = ScheduleSectionSerializer(schedule_sections, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ScheduleSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            schedule_section = ScheduleSection.objects.get(pk=pk)
        except ScheduleSection.DoesNotExist:
            return Response({'error': 'Schedule Section not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ScheduleSectionSerializer(schedule_section, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

