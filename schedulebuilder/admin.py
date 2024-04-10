from django.contrib import admin
from .models import Schedule, ScheduleFaculty, ScheduleRoom, ScheduleCourse, ScheduleSection
# Register your models here.


class ScheduleAdmin(admin.ModelAdmin):
    list_display  = ["id", "name", "semester", "department", "slug", "lastUpdated", "createdAt", "status"]


class ScheduleCourseAdmin(admin.ModelAdmin):
    list_display = ["id", "schedule", "code", "name", "number_of_sections", "number_of_labs"]


class ScheduleSectionAdmin(admin.ModelAdmin):
    list_display = ["id", "schedule", "schedule_course", "section_name", "sectionType", "faculty", "start_time", "end_time"]

class ScheduleFacultyAdmin(admin.ModelAdmin):
    list_display = ["id", "schedule", "name", "faculty"]

admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(ScheduleFaculty, ScheduleFacultyAdmin)
admin.site.register(ScheduleRoom)
admin.site.register(ScheduleCourse, ScheduleCourseAdmin)
admin.site.register(ScheduleSection, ScheduleSectionAdmin)