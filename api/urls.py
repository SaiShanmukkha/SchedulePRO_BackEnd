from main.views import CoursesView, FacultyView, course_corequisites_view
from django.urls import path
from schedulebuilder.views import SchedulesView, schedule_detail_view, schedule_faculty_view, schedule_course_view, schedule_section_view

urlpatterns = [
    path(route="courses/", view=CoursesView, name="Courses"),
    path(route="faculty/", view=FacultyView, name="Faculty"),
    path(route='courses/<int:course_id>/corequisites/', view=course_corequisites_view, name='course-corequisites'),
    path(route="schedules/", view=SchedulesView, name="Schedules"),
    path(route='schedules/<int:pk>/', view=schedule_detail_view, name='schedule-details'),
    path(route='schedules/<int:schedule_pk>/faculties/', view=schedule_faculty_view, name='schedule-faculty-list'),
    path(route='schedules/<int:schedule_pk>/faculties/<int:pk>/', view=schedule_faculty_view, name='schedule-faculty-detail'),
    path(route='schedules/<int:schedule_pk>/courses/', view=schedule_course_view, name='schedule_course_list'),
    path(route='schedules/<int:schedule_pk>/courses/<int:pk>/', view=schedule_course_view, name='schedule_course_detail'),
    path(route='schedules/<int:schedule_pk>/courses/<int:schedule_course_pk>/sections/', view=schedule_section_view, name='schedule_section_list'),
    path(route='schedules/<int:schedule_pk>/courses/<int:schedule_course_pk>/sections/<int:pk>/', view=schedule_section_view, name='schedule_section_detail'),
]



