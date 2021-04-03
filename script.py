from apps.core.models import BaseUser
from apps.ctf.models import Solve
from datetime import datetime
from django.db.models import Count
import pytz
from django.utils import timezone

# datetime.replace(tzinfo=pytz.UTC)
solve = Solve.objects.filter(created_date__gte=timezone.localtime().replace(hour=0,minute=0,second=0)).annotate(player=Count('user')).order_by('-player').select_related('user').first()

print(solve.user)
