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
def schedule_faculty_view(request, schedule_pk, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                schedule_faculty = ScheduleFaculty.objects.get(pk=pk, schedule_id=schedule_pk)
                serializer = ScheduleFacultySerializer(schedule_faculty)
            except ScheduleFaculty.DoesNotExist:
                return Response({'error': 'Schedule Faculty not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            schedule_faculties = ScheduleFaculty.objects.filter(schedule_id=schedule_pk)
            serializer = ScheduleFacultySerializer(schedule_faculties, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        data['schedule'] = schedule_pk  
        serializer = ScheduleFacultySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    elif request.method == 'PUT':
        try:
            schedule_faculty = ScheduleFaculty.objects.get(pk=pk, schedule_id=schedule_pk)
            serializer = ScheduleFacultySerializer(schedule_faculty, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ScheduleFaculty.DoesNotExist:
            return Response({'error': 'Schedule Faculty not found'}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'DELETE':
        try:
            schedule_faculty = ScheduleFaculty.objects.get(pk=pk, schedule_id=schedule_pk)
            schedule_faculty.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ScheduleFaculty.DoesNotExist:
            return Response({'error': 'Schedule Faculty not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def schedule_course_view(request, schedule_pk, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                schedule_course = ScheduleCourse.objects.get(pk=pk, schedule=schedule_pk)
                serializer = ScheduleCourseSerializer(schedule_course)
                return Response(serializer.data)
            except ScheduleCourse.DoesNotExist:
                return Response({'error': 'Schedule Course not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            schedule_courses = ScheduleCourse.objects.filter(schedule=schedule_pk)
            serializer = ScheduleCourseSerializer(schedule_courses, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ScheduleCourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(schedule_id=schedule_pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            schedule_course = ScheduleCourse.objects.get(pk=pk, schedule=schedule_pk)
        except ScheduleCourse.DoesNotExist:
            return Response({'error': 'Schedule Course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ScheduleCourseSerializer(schedule_course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            schedule_course = ScheduleCourse.objects.get(pk=pk, schedule=schedule_pk)
            schedule_course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ScheduleCourse.DoesNotExist:
            return Response({'error': 'Schedule Course not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def schedule_section_view(request, schedule_pk, schedule_course_pk, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                section = ScheduleSection.objects.get(pk=pk, schedule_course__schedule=schedule_pk, schedule_course=schedule_course_pk)
                serializer = ScheduleSectionSerializer(section)
                return Response(serializer.data)
            except ScheduleSection.DoesNotExist:
                return Response({'error': 'Schedule Section not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            sections = ScheduleSection.objects.filter(schedule_course__schedule=schedule_pk, schedule_course=schedule_course_pk)
            serializer = ScheduleSectionSerializer(sections, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ScheduleSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(schedule_course_id=schedule_course_pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            section = ScheduleSection.objects.get(pk=pk, schedule_course__schedule=schedule_pk, schedule_course=schedule_course_pk)
        except ScheduleSection.DoesNotExist:
            return Response({'error': 'Schedule Section not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ScheduleSectionSerializer(section, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            section = ScheduleSection.objects.get(pk=pk, schedule_course__schedule=schedule_pk, schedule_course=schedule_course_pk)
            section.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ScheduleSection.DoesNotExist:
            return Response({'error': 'Schedule Section not found'}, status=status.HTTP_404_NOT_FOUND)