from apps.api.views import BaseView
from .consts import (
    STATE_VISIBLE,
    STATE_HIDDEN
)
from .utils import *
from .models import (
    Challenge
)
from rest_framework.response import Response


class ChallengeList(BaseView):
    """
    Endpoint of challenges accepts only GET request
    """

    def get(self, request):
        user = request.user
        challenges = Challenge.objects.filter(
            state=STATE_VISIBLE).order_by('value')
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
        # flags = Flag.objects.filter(challenge=challenge)

        # for flag in flags:
        #     if submission == flag.content:
        #         if user.user_type == 'admin':

        #             return Response({'success': True, 'status': 'correct'})

        #         Solve.objects.create(
        #             user=user,
        #             challenge=challenge,
        #             submission=submission
        #         ).save()
        #         return Response({'success': True, 'status': 'correct'})
        # Submission.objects.create(
        #     user=user,
        #     challenge=challenge,
        #     submission=submission
        # ).save()

        return Response({'success': True, 'status': 'wrong', 'detail': 'Буруу байна'})


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
