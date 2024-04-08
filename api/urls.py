from main.views import IndexView, CoursesView, FacultyView
from django.urls import path

urlpatterns = [
    path(route="index/", view=IndexView, name="Index"),
    path(route="courses/", view=CoursesView, name="Courses"),
    path(route="faculty/", view=FacultyView, name="Faculty")
]
