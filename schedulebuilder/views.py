from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from schedulebuilder.utils import check_time_conflict
from .serializers import ScheduleCRUDSerializer, ScheduleSectionCRUDSerializer, ScheduleSerializer, ScheduleSectionSerializer, ScheduleCourseSerializer, ScheduleFacultySerializer
from .models import Schedule, ScheduleFaculty, ScheduleCourse, ScheduleSection
import pandas as pd
import io
from datetime import datetime
from django.db.models import Max, F
from .models import ScheduleCourse, ScheduleSection
from .serializers import ScheduleSectionSerializer

@api_view(['POST'])
def add_new_schedule_section(request, schedule_pk, schedule_course_pk):
    if request.method == 'POST':
        section_type = request.data.get('sectionType')
        if section_type not in ['Lab', 'Class']:
            return HttpResponse("Invalid Section Type.", status=404)

        sections = ScheduleSection.objects.filter(schedule_course_id=schedule_course_pk)

        sorted_sections = sections.order_by('section_name')

        last_section_same_type = sorted_sections.filter(sectionType=section_type).last()
        if(last_section_same_type):
            last_section_same_type_num = last_section_same_type.section_name[-1]
        else:
            last_section_same_type_num = 0
            
        if section_type == "Lab":
            new_section_name = f"Lab_{int(last_section_same_type_num)+1}"
        else:
            new_section_name = f"Sec_{int(last_section_same_type_num)+1}"
        

        new_section_data = {
            'schedule': schedule_pk,
            'schedule_course': schedule_course_pk,
            'sectionType': section_type,
            'section_name': new_section_name,
            'day': request.data.get('day'),
            'end_time': request.data.get('end_time'),
            'start_time': request.data.get('start_time')
        }

        serializer = ScheduleSectionCRUDSerializer(data=new_section_data)
        

        if serializer.is_valid():
            serializer.save()
            if(section_type == 'Class'):
                ScheduleCourse.objects.filter(id=schedule_course_pk).update(
                        number_of_sections=F('number_of_sections') + 1
                    )
            else:
                ScheduleCourse.objects.filter(id=schedule_course_pk).update(
                        number_of_labs=F('number_of_labs') + 1
                    )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def schedule_download(request, schedule_pk):
    if not Schedule.objects.filter(pk=schedule_pk).exists():
        return HttpResponse("Schedule not found.", status=404)
    
    schedule_sections = ScheduleSection.objects.filter(schedule=schedule_pk).select_related(
        'schedule_course__course__department',  
        'faculty__faculty__department' 
    )

    data = []
    for section in schedule_sections:
        course = section.schedule_course.course if section.schedule_course else None
        department_code = course.department.code if course and course.department else ''
        course_code = course.code if course else ''
        course_name = course.name if course else ''
        faculty_name = section.faculty.faculty.name if section.faculty and section.faculty.faculty else ''

        if section.start_time and section.end_time:
            time_range = f"{section.start_time.strftime('%H:%M')} - {section.end_time.strftime('%H:%M')}"
        else:
            time_range = ''

        data.append({
            'Departmentcode': department_code,
            'Coursecode': course_code,
            'Coursename': course_name,
            'Sectionname': section.section_name,
            'Facultyname': faculty_name,
            'Day': section.day or '',
            'Time': time_range
        })

    df = pd.DataFrame(data)
    
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Schedule', index=False)
    excel_buffer.seek(0)

    response = HttpResponse(excel_buffer.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="downloaded_file_{datetime.now()}.xlsx"'
    excel_buffer.close()
    
    return response


@api_view(['POST'])
def ScheduleSectionTimeAllotment(request):
        data = request.data
        
        print("\n\nData from request:\n", data, "\n\n")

        req_section_id = data.get('id')
        req_faculty_id = data.get('faculty')
        req_day = data.get('day')
        req_start_time = data.get('start_time')
        req_end_time = data.get('end_time')


        if req_section_id is None:
            return Response({"error": "Schedule section ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            schedule_section = ScheduleSection.objects.get(id=req_section_id)
        except ScheduleSection.DoesNotExist:
            return Response({"error": "ScheduleSection not found."}, status=status.HTTP_404_NOT_FOUND)

        print("\n\n", schedule_section.faculty, schedule_section.day, schedule_section.start_time, schedule_section.end_time, "\n\n")
        
        if (req_faculty_id is not None) and (req_day is None or req_start_time is None or req_end_time is None):
            existing_ss_time = schedule_section.day is not None and schedule_section.start_time is not None and schedule_section.end_time is not None

            # Subcase 1: No faculty assigned schedule section has no times
            if not schedule_section.faculty and not existing_ss_time:
                print("Case 1 <=> Subcase 1")
                sf = ScheduleFaculty.objects.get(id=req_faculty_id)
                schedule_section.faculty = sf
                schedule_section.save()
                ssd_serializer = ScheduleSectionSerializer(schedule_section)
                return Response({"message": "Faculty added successfully.", "data": ssd_serializer.data}, status=status.HTTP_200_OK)       
            
            # Subcase 2: only faculty in schedule section but no times
            elif schedule_section.faculty and not existing_ss_time:
                print("Case 1 <=> Subcase 2")
                sf = ScheduleFaculty.objects.get(id=req_faculty_id)
                schedule_section.faculty = sf
                schedule_section.save()
                ssd_serializer = ScheduleSectionSerializer(schedule_section)
                return Response({"message": "Faculty Updated successfully.", "data": ssd_serializer.data}, status=status.HTTP_200_OK)

            # Subcase 3: faculty empty but has schedulesectiontime
            elif not schedule_section.faculty and existing_ss_time:
                print("Case 1 <=> Subcase 3")

                conflicts = check_time_conflict(rsectionid=req_section_id, rfacultyid=req_faculty_id, rstarttime=schedule_section.start_time, rendtime=schedule_section.end_time, rday=schedule_section.day)
                if conflicts:
                    return Response({"error": "Time conflict detected with the new faculty assignments.", "conflicts":conflicts}, status=status.HTTP_400_BAD_REQUEST)

                sf = ScheduleFaculty.objects.get(id=req_faculty_id)
                schedule_section.faculty = sf
                schedule_section.save()
                ssd_serializer = ScheduleSectionSerializer(schedule_section)
                return Response({"message": "Faculty added successfully.", "data": ssd_serializer.data}, status=status.HTTP_200_OK)

            # Subcase 4: faculty not empty and has schedulesectiontime
            elif schedule_section.faculty and existing_ss_time:
                print("Case 1 <=> Subcase 4")

                conflicts = check_time_conflict(rsectionid=req_section_id, rfacultyid=req_faculty_id, rstarttime=schedule_section.start_time, rendtime=schedule_section.end_time, rday=schedule_section.day)
                if conflicts:
                    return Response({"error": "Time conflict detected with the new faculty assignments.", "conflicts":conflicts}, status=status.HTTP_400_BAD_REQUEST)
                
                sf = ScheduleFaculty.objects.get(id=req_faculty_id)
                schedule_section.faculty = sf
                schedule_section.save()
                ssd_serializer = ScheduleSectionSerializer(schedule_section)
                return Response({"message": "Faculty Updated successfully.", "data": ssd_serializer.data}, status=status.HTTP_200_OK)


        elif (req_faculty_id is None) and (req_day is not None and req_start_time is not None and req_end_time is not None):
            print("Case 2 Request")
            existing_ss_time = schedule_section.day is not None and schedule_section.start_time is not None and schedule_section.end_time is not None
            # Subcase 1: No faculty assigned schedule section has no times
            if not schedule_section.faculty and not existing_ss_time:
                print("Case 2 <=> Subcase 1")
                schedule_section.day = req_day
                schedule_section.start_time = req_start_time
                schedule_section.end_time = req_end_time
                schedule_section.save()
                ssd_serializer = ScheduleSectionSerializer(schedule_section)
                return Response({"message": "Added timings successfully.", "data": ssd_serializer.data}, status=status.HTTP_200_OK)

            # Subcase 2: No faculty assigned schedule section has times
            if not schedule_section.faculty and existing_ss_time:
                print("Case 2 <=> Subcase 2")
                schedule_section.day = req_day
                schedule_section.start_time = req_start_time
                schedule_section.end_time = req_end_time
                schedule_section.save()
                ssd_serializer = ScheduleSectionSerializer(schedule_section)
                return Response({"message": "Updated timings successfully.", "data": ssd_serializer.data}, status=status.HTTP_200_OK)

            # Subcase 3: faculty assigned schedule section also no times
            if schedule_section.faculty and not existing_ss_time:
                print("Case 2 <=> Subcase 3")
                conflicts = check_time_conflict(rsectionid=req_section_id, rfacultyid=schedule_section.faculty, rstarttime=req_start_time, rendtime=req_end_time, rday=req_day)
                if conflicts:
                    return Response({"error": "Time conflict detected with the faculty assignments.", "conflicts":conflicts}, status=status.HTTP_400_BAD_REQUEST)
                schedule_section.day = req_day
                schedule_section.start_time = req_start_time
                schedule_section.end_time = req_end_time
                schedule_section.save()
                ssd_serializer = ScheduleSectionSerializer(schedule_section)
                return Response({"message": "Added timings successfully.", "data": ssd_serializer.data}, status=status.HTTP_200_OK)

            # Subcase 4: Faculty assigned and schedule section also has times
            if schedule_section.faculty and existing_ss_time:
                print("Case 2 <=> Subcase 4")
                conflicts = check_time_conflict(rsectionid=req_section_id, rfacultyid=schedule_section.faculty, rstarttime=req_start_time, rendtime=req_end_time, rday=req_day)
                if conflicts:
                    return Response({"error": "Time conflict detected with the faculty assignments.", "conflicts":conflicts}, status=status.HTTP_400_BAD_REQUEST)
                schedule_section.day = req_day
                schedule_section.start_time = req_start_time
                schedule_section.end_time = req_end_time
                schedule_section.save()
                ssd_serializer = ScheduleSectionSerializer(schedule_section)
                return Response({"message": "Updated timings successfully.", "data": ssd_serializer.data}, status=status.HTTP_200_OK)

        elif (req_faculty_id is not None) and (req_day is not None) and (req_start_time is not None) and (req_end_time is not None):
            print("Case 3 Request")
            existing_ss_time = schedule_section.day is not None and schedule_section.start_time is not None and schedule_section.end_time is not None
        
            print("Case 3")
            conflicts = check_time_conflict(rsectionid=req_section_id, rfacultyid=req_faculty_id, rstarttime=req_start_time, rendtime=req_end_time, rday=req_day)
            if conflicts:
                return Response({"error": "Time conflict detected with the faculty assignments.", "conflicts":conflicts}, status=status.HTTP_400_BAD_REQUEST)
            
            sf = ScheduleFaculty.objects.get(id=req_faculty_id)
            schedule_section.faculty = sf
            schedule_section.day = req_day
            schedule_section.start_time = req_start_time
            schedule_section.end_time = req_end_time
            schedule_section.save()
            ssd_serializer = ScheduleSectionSerializer(schedule_section)
            if existing_ss_time:
                Response({"message": "Updated faculty and timings successfully.", "data": ssd_serializer.data}, status=status.HTTP_200_OK)

            return Response({"message": "Added faculty and timings successfully.", "data": ssd_serializer.data}, status=status.HTTP_200_OK)

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
        serializer = ScheduleCRUDSerializer(data=request.data)
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
        schedule_course = get_object_or_404(ScheduleCourse, pk=schedule_course.pk)
        if schedule_course.number_of_labs + schedule_course.number_of_sections == 1:
            return Response({'error': 'Only one Section in this Course. Please delete course.'}, status=status.HTTP_400_BAD_REQUEST)
        section = get_object_or_404(ScheduleSection, pk=pk, schedule_course=schedule_course)
        section.delete()
        if(section.sectionType=='Class'):
            ScheduleCourse.objects.filter(id=schedule_course.pk).update(
                    number_of_sections=F('number_of_sections') - 1
                )
        else:
            ScheduleCourse.objects.filter(id=schedule_course.pk).update(
                    number_of_labs=F('number_of_labs') - 1
                )
            
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



