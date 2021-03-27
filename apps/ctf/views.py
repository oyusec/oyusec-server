from datetime import datetime, timezone
from rest_framework.response import Response
from apps.api.views import BaseView
from .consts import *
from .utils import *
from .models import (
    Challenge
)
from apps.competition.consts import *
from apps.competition.models import (
    Competition,
    CompetitionUser
)
from apps.core.utils import convert_to_localtime, td_format


class ChallengeList(BaseView):
    """
    Endpoint of public challenges
    """

    def get(self, request):
        user = request.user
        challenges = Challenge.objects.filter(
            state=STATE_VISIBLE, competition=None).order_by('value')
        response = self.serialize(challenges, user)
        return Response({'success': True, 'data': response})

    def serialize(self, challenges, user):
        ret = []

        for challenge in challenges:
            ret.append({
                'name': challenge.name,
                'value': challenge.value,
                'description': challenge.description,
                'id': challenge.uuid,
                'status': 'unsolved',
                'state': challenge.state,
                'category': challenge.category,
                'competition': False
            })
            # if challenge.category not in ret.keys():
            #     ret[challenge.category] = []

            # ret[challenge.category].append(data)
        return ret


class ChallengeAttempt(BaseView):
    """
    Endpoint of checking flag
    """

    def get(self, request):
        user = request.user

        return Response({'success': True, 'data': 'hey'})

    def post(self, request):
        user = request.user
        challenge_id = request.data['challenge_id']

        if not user.is_authenticated:
            return Response({'success': False, 'detail': AUTHENTICATION_REQUIRED})
        challenge = get_chall(challenge_id)

        # Checking user can submit flag or not
        status, message = challenge.check_valid(
            user=user, challenge=challenge, request=request)

        if not status:
            return Response({
                'success': False,
                'detail': message
            })

        # Checking challenge from competition or not
        if challenge.competition:
            # I hope this will never happen, just in case
            if challenge.competition.status != COMPETITION_LIVE:
                return Response({
                    'success': False,
                    'detail': 'Тэмцээн эхлээгүй байна'
                })

            status, message = challenge.attempt(challenge, request)

            # If user submit flag and it's correct, then we register user as participant
            if status:
                compUser = CompetitionUser.objects.filter(
                    user=user, competition=challenge.competition)

                if not compUser:
                    compUser = CompetitionUser.objects.create(
                        user=user,
                        competition=challenge.competition,
                    )

                challenge.solve(
                    user=user, challenge=challenge, request=request
                )

        else:
            status, message = challenge.attempt(challenge, request)
            if status:
                challenge.solve(
                    user=user, challenge=challenge, request=request
                )

        return Response({
            "success": True,
            "status": "correct" if status else "incorrect",
            "detail": message
        })


class ChallengeSolves(BaseView):
    def get(self, request, uuid):
        try:
            challenge = Challenge.objects.get(uuid=uuid)
        except:
            return Response({
                'success': False,
                'detail': NOT_FOUND
            })
        if challenge.state == STATE_HIDDEN:
            return Response({
                'success': False,
                'detail': NOT_FOUND
            })

        response = self.serialize(challenge)

        return Response({
            'success': True,
            'data': response
        })

    def serialize(self, challenge):
        ret = []
        for solve in Solve.objects.filter(challenge=challenge).order_by('-created_date'):
            ret.append({
                'slug': solve.user.slug,
                'username': solve.user.username,
                'time': td_format(datetime.now(timezone.utc) - solve.created_date),
            })

        return ret


class ChallengesSolves(BaseView):
    def get(self, request):
        challenges = Challenge.objects.filter(
            state=STATE_VISIBLE
        )
        response = self.serialize(challenges)

        return Response({'success': True, 'data': response})

    def serialize(self, challenges):
        ret = []
        for challenge in challenges:
            solves = Solve.objects.filter(challenge=challenge).count()
            ret.append({
                'challengeID': challenge.uuid,
                'solves': solves
            })
        return ret


class Scoreboard(BaseView):

    def get(self, request):
        standings = get_standings()
        return Response({'success': True, 'data': standings})
