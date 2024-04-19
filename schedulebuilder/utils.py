from datetime import datetime
from django.db.models import Q
from main.models import CourseCorequisite
from schedulebuilder.models import ScheduleSection

def check_time_conflict(rsectionid, rfacultyid, rday, rstarttime, rendtime):
    if isinstance(rstarttime, str):
        rstarttime = datetime.strptime(rstarttime, '%H:%M').time()
    if isinstance(rendtime, str):
        rendtime = datetime.strptime(rendtime, '%H:%M').time()

    condition_1 = Q(start_time__lte=rstarttime, end_time__gte=rendtime) 
    condition_2 = Q(start_time__gte=rstarttime, end_time__lte=rendtime) 
    condition_3 = Q(start_time__lt=rstarttime, end_time__gt=rstarttime, end_time__lte=rendtime) 
    condition_4 = Q(start_time__gte=rstarttime, start_time__lt=rendtime, end_time__gt=rendtime)  

    combined_conditions = condition_1 | condition_2 | condition_3 | condition_4

    conflicts = ScheduleSection.objects.filter(
        faculty__id=rfacultyid,
        day__contains=rday,
        ).exclude(id=rsectionid).filter(combined_conditions).exists()
    
    
    if conflicts:
        print("Faculty Conflict")
        return True

    schedule_section = ScheduleSection.objects.select_related('schedule_course__course').get(id=rsectionid)
    if not schedule_section or not schedule_section.schedule_course or not schedule_section.schedule_course.course:
        return False  
    primary_course_id = schedule_section.schedule_course.course.id
    direct_corequisites = CourseCorequisite.objects.filter(course_id=primary_course_id)
    direct_corequisite_ids = [c.corequisite.id for c in direct_corequisites if c.corequisite]
    reverse_corequisites = CourseCorequisite.objects.filter(corequisite_id=primary_course_id)
    reverse_corequisite_ids = [c.course.id for c in reverse_corequisites if c.course]
    all_corequisite_ids = set(direct_corequisite_ids + reverse_corequisite_ids)

    if all_corequisite_ids:
        conflicts = ScheduleSection.objects.filter(
            day__contains=rday,
            schedule_course__course__id__in=all_corequisite_ids
        ).exclude(id=rsectionid).filter(
            Q(start_time__lte=rstarttime, end_time__gte=rendtime) |  
            Q(start_time__gte=rstarttime, end_time__lte=rendtime) | 
            Q(start_time__lt=rstarttime, end_time__gt=rstarttime, end_time__lte=rendtime) | 
            Q(start_time__gte=rstarttime, start_time__lt=rendtime, end_time__gt=rendtime)  
        ).exists()

        if conflicts:
            print("Corequisite & Course Time Conflict")
            return True


    return False

