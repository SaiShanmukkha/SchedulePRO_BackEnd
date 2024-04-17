from datetime import datetime
from django.db.models import Q


def check_time_conflict(rfacultyid, rstarttime, rendtime, rday)->bool:
    input_days = list(rday)

    if isinstance(rstarttime, str):
        rstarttime = datetime.strptime(rstarttime, '%H:%M').time()
    if isinstance(rendtime, str):
        rendtime = datetime.strptime(rendtime, '%H:%M').time()

    conflict_found = False
    for input_day in input_days:
        # conflicts = ScheduleSectionTime.objects.filter(
        #     schedule_section__faculty__id=rfacultyid
        # ).filter(
        #     Q(start_time__lt=rendtime, end_time__gt=rstarttime)
        # )

        conflicts = conflicts.filter(day__contains=input_day)

        if conflicts.exists():
            conflict_found = True
            break

    return conflict_found

if __name__ == "__main__":
    rfacultyid = 37
    rstarttime = '12:00'
    rendtime = '15:00'
    rday = 'MWR'
