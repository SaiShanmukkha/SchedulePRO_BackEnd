from django.contrib import admin
from .models import Schedule, ScheduleFaculty, ScheduleRoom, ScheduleCourse, ScheduleSection
# Register your models here.

admin.site.register(Schedule)
admin.site.register(ScheduleFaculty)
admin.site.register(ScheduleRoom)
admin.site.register(ScheduleCourse)
admin.site.register(ScheduleSection)