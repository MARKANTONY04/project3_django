# chat gpt helped recreate this file from previous iteration to fit with the new app

from datetime import datetime, timedelta, time as dtime
from .models import Reservation

# Allowed slot starts
SLOT_STARTS = [dtime(12,0), dtime(14,0), dtime(16,0), dtime(18,0), dtime(20,0)]
SLOT_DURATION = timedelta(hours=2)
MAX_TABLES_PER_GROUP = 3  # per table size group

def overlap(start1, end1, start2, end2):
    """Return True if time windows [start1,end1) and [start2,end2) overlap."""
    return start1 < end2 and start2 < end1

def table_group(guests):
    """Return table group based on number of guests."""
    if guests <= 2:
        return 2
    elif guests <= 4:
        return 4
    elif guests <= 6:
        return 6
    elif guests <= 8:
        return 8
    else:
        return 10

def is_table_available(date, time_obj, guests, exclude_id=None):
    """Check table availability."""
    if time_obj not in SLOT_STARTS:
        return False  # invalid slot

    req_start = datetime.combine(date, time_obj)
    req_end = req_start + SLOT_DURATION
    group = table_group(guests)

    overlapping_count = 0
    qs = Reservation.objects.filter(date=date)
    if exclude_id:
        qs = qs.exclude(pk=exclude_id)

    for r in qs:
        r_start = datetime.combine(r.date, r.time)
        r_end = r_start + SLOT_DURATION
        if r.table_group() == group and overlap(req_start, req_end, r_start, r_end):
            overlapping_count += 1

    return overlapping_count < MAX_TABLES_PER_GROUP


