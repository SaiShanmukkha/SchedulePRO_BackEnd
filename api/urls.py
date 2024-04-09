from main.views import CoursesView, FacultyView
from django.urls import path
from schedulebuilder.views import SchedulesView, schedule_detail_view, schedule_section_view, schedule_course_view, schedule_faculty_view

urlpatterns = [
    path(route="courses/", view=CoursesView, name="Courses"),
    path(route="faculty/", view=FacultyView, name="Faculty"),
    path(route="schedules/", view=SchedulesView, name="Schedules"),
    path(route='schedules/<int:pk>/', view=schedule_detail_view, name='schedule-detail'),
    path(route='schedule-courses/', view=schedule_course_view, name='schedule-courses-list'),
    path(route='schedule-courses/<int:pk>/', view=schedule_course_view, name='schedule-course-detail'),
    path(route='schedule-faculties/', view=schedule_faculty_view, name='schedule-faculties-list'),
    path(route='schedule-faculties/<int:pk>/', view=schedule_faculty_view, name='schedule-faculty-detail'),
    path(route='schedule-sections/', view=schedule_section_view, name='schedule-sections-list'),
    path(route='schedule-sections/<int:pk>/', view=schedule_section_view, name='schedule-section-detail'),
]



