import pytz
from django.utils import timezone


def is_admin(request):
    if not request.user.is_authenticated or not request.user.user_type == 'admin':
        return False

    return True


def convert_to_localtime(utctime):

    fmt = '%Y-%m-%d, %H:%M'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz.strftime(fmt)
