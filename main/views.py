from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course, Faculty
from .serializers import CourseSerealizer, FacultySerealizer

@api_view(['GET'])
def IndexView(request):
    return Response("Index")


@api_view(['GET'])
def CoursesView(request):
    coursesObjs = Course.objects.all()
    serealized_courses = CourseSerealizer(coursesObjs, many=True)
    return Response(serealized_courses.data)


@api_view(['GET'])
def FacultyView(request):
    facultyObjs = Faculty.objects.all()
    serealized_faculty = FacultySerealizer(facultyObjs, many=True)
    return Response(serealized_faculty.data)