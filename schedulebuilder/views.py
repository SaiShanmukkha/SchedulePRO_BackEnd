from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from schedulebuilder.utils import check_time_conflict
from .serializers import ScheduleSectionCRUDSerializer, ScheduleSerializer, ScheduleSectionSerializer, ScheduleCourseSerializer, ScheduleFacultySerializer
from .models import Schedule, ScheduleFaculty, ScheduleCourse, ScheduleSection



@api_view(['POST'])
def ScheduleSectionTimeAllotment(request):
        data = request.data
        req_section_id = data.get('schedule_section')
        req_faculty_id = data.get('faculty')
        req_day = data.get('day')
        req_start_time = data.get('start_time')
        req_end_time = data.get('end_time')

        print("\n\n", data, "\n\n")

        if req_section_id is None:
            return Response({"error": "Schedule section ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            schedule_section = ScheduleSection.objects.get(id=req_section_id)
        except ScheduleSection.DoesNotExist:
            return Response({"error": "ScheduleSection not found."}, status=status.HTTP_404_NOT_FOUND)

        
        if (req_faculty_id is not None) and (req_day is None or req_start_time is None or req_end_time is None):

            existing_schedule_section_times = ScheduleSectionTime.objects.filter(schedule_section__id=req_section_id)

            # Subcase 1: No faculty assigned schedule section also no times
            if not schedule_section.faculty and not existing_schedule_section_times:
                print("Case 1 <=> Subcase 1")
                sf = ScheduleFaculty.objects.get(id=req_faculty_id)
                schedule_section.faculty = sf
                schedule_section.save()
                return Response({"message": "Faculty added successfully."}, status=status.HTTP_200_OK)       
            
            # Subcase 2: only faculty in schedule section but no times
            elif schedule_section.faculty and not existing_schedule_section_times:
                print("Case 1 <=> Subcase 2")
                sf = ScheduleFaculty.objects.get(id=req_faculty_id)
                schedule_section.faculty = sf
                schedule_section.save()
                return Response({"message": "Faculty Updated successfully."}, status=status.HTTP_200_OK)

            # Subcase 3: faculty empty but has schedulesectiontime
            elif not schedule_section.faculty and existing_schedule_section_times:
                print("Case 1 <=> Subcase 3")

                # conflict = check_time_conflict(rfacultyid=req_faculty_id, rstarttime, rendtime, rday)
                conflict = False
                if conflict:
                    return Response({"error": "Time conflict detected with the new faculty assignments."}, status=status.HTTP_400_BAD_REQUEST)



                return Response({"message": "Faculty added successfully."}, status=status.HTTP_200_OK)

            # Subcase 4: faculty not empty and has schedulesectiontime
            elif schedule_section.faculty and existing_schedule_section_times:
                print("Case 1 <=> Subcase 4")

                conflict = False
                if conflict:
                    return Response({"error": "Time conflict detected with the new faculty assignments."}, status=status.HTTP_400_BAD_REQUEST)

                return Response({"message": "Faculty Updated successfully."}, status=status.HTTP_200_OK)



        # elif (faculty_id is None) and (day is not None and start_time is not None and end_time is not None):
        #     print("Case 2 Request")

        # elif (faculty_id is not None) and (day is not None) and (start_time is not None) and (end_time is not None):
        #     print("Case 3 Request")

        else:
            return Response({"error": "Invalid Data."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


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

@api_view(['GET'])
def schedule_section_list(request, schedule_pk):
    if request.method == 'GET':
        sections = ScheduleSection.objects.filter(schedule_course__schedule=schedule_pk)
        serializer = ScheduleSectionSerializer(sections, many=True)
        return Response(serializer.data)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def schedule_section_view(request, schedule_pk, schedule_course_pk, pk=None):
    schedule = get_object_or_404(Schedule, pk=schedule_pk)
    schedule_course = get_object_or_404(ScheduleCourse, pk=schedule_course_pk, schedule=schedule)

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
        if isinstance(request.data, list):
            serializer = ScheduleSectionCRUDSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save(schedule_course_id=schedule_course_pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ScheduleSectionCRUDSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(schedule_course_id=schedule_course_pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'PUT':
        section = get_object_or_404(ScheduleSection, pk=pk, schedule_course=schedule_course)
        crud_serializer = ScheduleSectionCRUDSerializer(section, data=request.data, partial=True) # Allow partial updates
        if crud_serializer.is_valid():
            saved_section = crud_serializer.save()
            
            response_serializer = ScheduleSectionSerializer(saved_section)
            return Response(response_serializer.data)
    
        return Response(crud_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        section = get_object_or_404(ScheduleSection, pk=pk, schedule_course=schedule_course)
        section.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def schedule_section_time_view(request, schedule_pk, schedule_course_pk, schedule_section_pk):
   
#     if request.method == 'GET':
#         times = ScheduleSectionTime.objects.filter(
#             schedule_id=schedule_pk,
#             schedule_course_id=schedule_course_pk,
#             schedule_section_id=schedule_section_pk
#         )
#         serializer = ScheduleSectionTimeSerializer(times, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = CUSTOMScheduleSectionTimeSerializer(data=request.data)
#         if serializer.is_valid():
#             faculty_id = serializer.validated_data.get('schedule_section').faculty.id
#             day = serializer.validated_data.get('day')
#             start_time = serializer.validated_data.get('start_time')
#             end_time = serializer.validated_data.get('end_time')

#             if check_faculty_time_collision(faculty_id, day, start_time, end_time):
#                 return Response({'error': 'Scheduling conflict detected for the faculty.'}, status=status.HTTP_409_CONFLICT)

#             serializer.save(schedule_id=schedule_pk, schedule_course_id=schedule_course_pk, schedule_section_id=schedule_section_pk)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'PUT':
#         time_entry = ScheduleSectionTime.objects.filter(
#             pk=request.data.get('id', 0),
#             schedule_id=schedule_pk,
#             schedule_course_id=schedule_course_pk,
#             schedule_section_id=schedule_section_pk
#         ).first()

#         if not time_entry:
#             return Response({'error': 'Time entry not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = CUSTOMScheduleSectionTimeSerializer(time_entry, data=request.data, partial=True) # Allow partial updates
#         if serializer.is_valid():
#             faculty_id = serializer.validated_data.get('schedule_section').faculty.id
#             day = serializer.validated_data.get('day')
#             start_time = serializer.validated_data.get('start_time')
#             end_time = serializer.validated_data.get('end_time')

#             if check_faculty_time_collision(faculty_id, day, start_time, end_time, existing_id=time_entry.id):
#                 return Response({'error': 'Scheduling conflict detected for the faculty.'}, status=status.HTTP_409_CONFLICT)

#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
#     elif request.method == 'DELETE':
#         try:
#             time_entry = ScheduleSectionTime.objects.get(
#                 pk=request.data['id'],
#                 schedule_id=schedule_pk,
#                 schedule_course_id=schedule_course_pk,
#                 schedule_section_id=schedule_section_pk
#             )
#             time_entry.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except ScheduleSectionTime.DoesNotExist:
#             return Response({'error': 'Time entry not found'}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# def schedule_section_time_list(request, schedule_pk):
#     if request.method == 'GET':
#         sections_time = ScheduleSectionTime.objects.filter(schedule_course__schedule=schedule_pk)
#         serializer = ScheduleSectionTimeSerializer(sections_time, many=True)
#         return Response(serializer.data)