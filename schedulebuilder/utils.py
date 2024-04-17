from datetime import datetime
from django.db.models import Q
from schedulebuilder.models import ScheduleSection

def check_time_conflict(rsectionid, rfacultyid, rday, rstarttime, rendtime):
    if isinstance(rstarttime, str):
        rstarttime = datetime.strptime(rstarttime, '%H:%M').time()
    if isinstance(rendtime, str):
        rendtime = datetime.strptime(rendtime, '%H:%M').time()

    condition_1 = Q(start_time__lte=rstarttime, end_time__gte=rendtime)  # Completely within the range
    condition_2 = Q(start_time__gte=rstarttime, end_time__lte=rendtime)  # Enveloping the range
    condition_3 = Q(start_time__lt=rstarttime, end_time__gt=rstarttime, end_time__lte=rendtime)  # Overlapping start
    condition_4 = Q(start_time__gte=rstarttime, start_time__lt=rendtime, end_time__gt=rendtime)  # Overlapping end

    combined_conditions = condition_1 | condition_2 | condition_3 | condition_4

    conflicts = ScheduleSection.objects.filter(
        faculty__id=rfacultyid,
        day__contains=rday,
        ).exclude(id=rsectionid).filter(combined_conditions).exists()

    return conflicts


if __name__ == "__main__":
    rfacultyid = 37
    rstarttime = '12:00'
    rendtime = '15:00'
    rday = 'MWR'
