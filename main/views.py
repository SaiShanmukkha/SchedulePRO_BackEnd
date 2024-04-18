from rest_framework.decorators import api_view
from rest_framework.response import Response

from schedulebuilder.models import ScheduleCourse
from .models import Course, CourseCorequisite, Department, Faculty, Semester
from .serializers import CourseCorequisiteSerializer, CourseSerializer, DepartmentSerializer, FacultySerializer, SemesterSerializer

@api_view(['GET'])
def CourseCorequisitesListView(request):
    course_ids = request.query_params.get('course_ids')
    if course_ids:
        course_ids = [int(id) for id in course_ids.split(',')]
        corequisites = CourseCorequisite.objects.filter(course_id__in=course_ids)
    
    serializer = CourseCorequisiteSerializer(corequisites, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def CourseCorequisitesView(request, course_id):
    corequisites = CourseCorequisite.objects.filter(course_id=course_id)
    serializer = CourseCorequisiteSerializer(corequisites, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def CoursesView(request):
    coursesObjs = Course.objects.all()
    serealized_courses = CourseSerializer(coursesObjs, many=True)
    return Response(serealized_courses.data)

@api_view(['GET'])
def SemesterView(request):
    semesters = Semester.objects.all()
    serializer = SemesterSerializer(semesters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def FacultyView(request):
    facultyObjs = Faculty.objects.all()
    serealized_faculty = FacultySerializer(facultyObjs, many=True)
    return Response(serealized_faculty.data)

@api_view(['GET'])
def DepartmentsView(request):
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def course_corequisites_view(request, scheduleId):
    schedule_courses = ScheduleCourse.objects.filter(schedule=scheduleId).select_related('course')

    course_corequisites_data = []

    for sc in schedule_courses:
        if sc.course: 
            corequisites = CourseCorequisite.objects.filter(course=sc.course)

            if not corequisites:
                continue

            serializer = CourseCorequisiteSerializer(corequisites, many=True)

            grouped = {'mandatory': [], 'choice': []}
            for item in serializer.data:
                if item['Type'].lower() == 'mandatory':
                    grouped['mandatory'].append(item['corequisite'])
                else:
                    grouped['choice'].append(item['corequisite'])

            course_corequisites_data.append({
                'course_info': {
                    'id': sc.course.id,
                    'name': sc.course.name,
                    'code': sc.course.code,
                    'department': sc.course.department.name
                },
                'corequisites': grouped
            })

    return Response(course_corequisites_data)