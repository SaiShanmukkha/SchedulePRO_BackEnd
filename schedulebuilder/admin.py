from django.contrib import admin
from .models import Schedule, ScheduleFaculty, ScheduleRoom, ScheduleCourse, ScheduleSection
# Register your models here.


class ScheduleAdmin(admin.ModelAdmin):
    list_display  = ["name", "semester", "lastUpdated", "createdAt", "status"]


admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(ScheduleFaculty)
admin.site.register(ScheduleRoom)
admin.site.register(ScheduleCourse)
admin.site.register(ScheduleSection)