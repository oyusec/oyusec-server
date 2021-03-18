from django.utils import timezone
from .consts import *


def get_enrollment(data):
    if data == ENROLLMENT_SOLO:
        return ENROLLMENT_SOLO_MN
    elif data == ENROLLMENT_TEAM:
        return ENROLLMENT_TEAM_MN
    elif data == ENROLLMENT_SOLO_MN:
        return ENROLLMENT_SOLO
    elif data == ENROLLMENT_TEAM_MN:
        return ENROLLMENT_TEAM


def get_status(data):
    if data == COMPETITION_LIVE:
        return 'Шууд'
    elif data == COMPETITION_COMING:
        return 'Удахгүй'
    elif data == COMPETITION_ARCHIVE:
        return 'Дууссан'


def get_timeleft(data):
    return int((data - timezone.now()).total_seconds())


def get_days_hours_minutes(data):
    return data.days, data.seconds // 3600, (data.seconds // 60) % 60
