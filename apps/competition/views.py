from django.shortcuts import get_object_or_404
from django.utils.timezone import localdate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.core.models import (
    BaseUser,
    BaseUserProfile
)
from apps.core.utils import *
from apps.ctf.models import (
    Challenge
)
from apps.api.views import BaseView

from .models import (
    CompetitionUser,
    Competition,
)
from .utils import *

from .consts import *


class Competitions(BaseView):
    def get(self, request):
        response = self.serialize()

        return Response({
            'success': True,
            'data': response
        })

    def serialize(self):
        result = {
            'live': [],
            'upcoming': [],
            'archive': []
        }
        for _ in Competition.objects.all():
            result[_.status].append({
                'name': _.name,
                'description': _.description,
                'id': _.uuid,
                'photo': _.photo,
                'slug': _.slug,
                'start_date': convert_to_localtime(_.start_date),
                'end_date': convert_to_localtime(_.end_date),
            })

        return result


class CompetitionView(BaseView):
    def get(self, request, slug):
        competition = get_object_or_404(Competition, slug=slug)
        response = self.serialize(competition)

        return Response({'success': True, 'data': response})

    def serialize(self, competition):
        result = {
            'challenges': [],
            'name': competition.name,
            'description': competition.description,
            'photo': competition.photo,
            'rule': competition.rule,
            'prize': competition.prize,
            'location': competition.location,
            'enrollment': get_enrollment(competition.enrollment),
            'start_date': convert_to_localtime(competition.start_date),
            'end_date': convert_to_localtime(competition.end_date),
            'status': get_status(competition.status),
        }

        if competition.status == COMPETITION_UPCOMING:
            result['time_left'] = get_timeleft(competition.start_date)
            return result

        for challenge in Challenge.objects.filter(competition=competition):
            result['challenges'].append({
                'name': challenge.name,
                'value': challenge.value,
                'description': challenge.description,
                'id': challenge.uuid,
                'status': 'unsolved',
                'state': challenge.state,
                'category': challenge.category,
            })
            # if challenge.category not in ret.keys():
            #     ret[challenge.category] = []

            # ret[challenge.category].append(data)
        return result
        # for challenge
        # Challenge.objects.filter(competition=competition)
        # return []
