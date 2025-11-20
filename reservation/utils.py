# chat gpt helped recreate this file from previous iteration to fit with the new app

from datetime import datetime, timedelta, time as dtime
from .models import Reservation

# Allowed slot starts
SLOT_STARTS = [dtime(12,0), dtime(14,0), dtime(16,0), dtime(18,0), dtime(20,0)]
SLOT_DURATION = timedelta(hours=2)
MAX_TABLES_PER_GROUP = 3

def overlap(start1, end1, start2, end2):
    """Return True if time windows [start1,end1) and [start2,end2) overlap."""
    return start1 < end2 and start2 < end1

def is_table_available(date, time_obj, guests):
    """
    Check whether a table is available for given date, time (datetime.time) and guests.
    Enforces 3 tables per table-size group per overlapping 2-hour window.
    """
    # ensure slot start is one of allowed starts
    if time_obj not in SLOT_STARTS:
        return False  # invalid slot

    # compute requested window as datetimes
    req_start = datetime.combine(date, time_obj)
    req_end = req_start + SLOT_DURATION

    # find the table-group for requested guests
    if guests <= 2:
        group = 2
    elif guests <= 4:
        group = 4
    elif guests <= 6:
        group = 6
    elif guests <= 8:
        group = 8
    else:
        group = 10

    # count overlapping reservations on same date whose table_group == group
    overlapping_count = 0

    existing_qs = Reservation.objects.filter(date=date)

    for r in existing_qs:
        try:
            r_start = datetime.combine(r.date, r.time)
        except Exception:
            continue
        r_end = r_start + SLOT_DURATION

        # if reservation belongs to the same table group
        if r.table_group() == group:
            if overlap(req_start, req_end, r_start, r_end):
                overlapping_count += 1

    return overlapping_count < MAX_TABLES_PER_GROUP
