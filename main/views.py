from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course, CourseCorequisite, Faculty
from .serializers import CourseCorequisiteSerializer, CourseSerializer, FacultySerializer


@api_view(['GET'])
def CoursesView(request):
    coursesObjs = Course.objects.all()
    serealized_courses = CourseSerializer(coursesObjs, many=True)
    return Response(serealized_courses.data)


@api_view(['GET'])
def FacultyView(request):
    facultyObjs = Faculty.objects.all()
    serealized_faculty = FacultySerializer(facultyObjs, many=True)
    return Response(serealized_faculty.data)

@api_view(['GET'])
def course_corequisites_view(request, course_id):
    try:
        corequisites = CourseCorequisite.objects.filter(course_id=course_id)
        serializer = CourseCorequisiteSerializer(corequisites, many=True)
        return Response(serializer.data)
    except CourseCorequisite.DoesNotExist:
        return Response({'error': 'Course not found or no corequisites available.'}, status=404)