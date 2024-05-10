from main.views import CoursesView, FacultyView, SemesterView, CourseCorequisitesView, DepartmentsView, course_corequisites_view
from django.urls import path
from schedulebuilder.views import ScheduleSectionTimeAllotment, SchedulesView, add_new_schedule_section, schedule_detail_view, schedule_download, schedule_faculty_view, schedule_course_view, schedule_section_remove_faculty, schedule_section_remove_schtime, schedule_section_view, schedule_section_list

urlpatterns = [
    path(route="courses/", view=CoursesView, name="Courses"),
    path(route="faculty/", view=FacultyView, name="Faculty"),
    path(route='departments/', view=DepartmentsView, name='departments'),
    path(route='semesters/', view=SemesterView, name='semesters'),
    path(route='courses/<int:course_id>/corequisites/', view=CourseCorequisitesView, name='course-corequisites'),
    path(route='course-corequisites/schedule/<int:scheduleId>/', view=course_corequisites_view, name='schedule-course-corequisites'),
    path(route="schedules/", view=SchedulesView, name="Schedules"),
    path(route='schedules/<int:pk>/', view=schedule_detail_view, name='schedule-details'),
    path(route='schedules/<int:schedule_pk>/download/', view=schedule_download, name='schedule-download'),
    path(route='schedules/<int:schedule_pk>/faculties/', view=schedule_faculty_view, name='schedule-faculty-list'),
    path(route='schedules/<int:schedule_pk>/faculties/<int:pk>/', view=schedule_faculty_view, name='schedule-faculty-detail'),
    path(route='schedules/<int:schedule_pk>/courses/', view=schedule_course_view, name='schedule_course_list'),
    path(route='schedules/<int:schedule_pk>/courses/<int:pk>/', view=schedule_course_view, name='schedule_course_detail'),
    path(route='schedules/<int:schedule_pk>/courses/<int:schedule_course_pk>/new-section', view=add_new_schedule_section, name='add_schedule_section'),
    path(route='schedules/<int:schedule_pk>/sections/', view=schedule_section_list, name='schedule_section_list'),
    path(route='schedules/<int:schedule_pk>/courses/<int:schedule_course_pk>/sections/', view=schedule_section_view, name='schedule_sections'),
    path(route='schedules/<int:schedule_pk>/courses/<int:schedule_course_pk>/sections/<int:pk>/', view=schedule_section_view, name='schedule_section_detail'),
    path(route='schedules/<int:schedule_pk>/courses/<int:schedule_course_pk>/sections/<int:schedule_section_pk>/remove-faculty/', view=schedule_section_remove_faculty, name='schedule_section_rmfac'),
    path(route='schedules/<int:schedule_pk>/courses/<int:schedule_course_pk>/sections/<int:schedule_section_pk>/remove-schtime/', view=schedule_section_remove_schtime, name='schedule_section_rmschtime'),
    path(route='schedules/schedule-section-times/', view=ScheduleSectionTimeAllotment, name='schedule-section-times'),
]

