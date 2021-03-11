from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.shortcuts import get_object_or_404

from apps.core.models import (
    BaseUser,
    BaseUserProfile
)

from apps.ctf.models import (
    StandardChallenge,
    DynamicChallenge,
    Submission,
    Solve,
    Challenge,
    Config,
    Flag,
    Hint,
    Tag,
)

from apps.ctf.consts import (
    STATE_VISIBLE,
    STATE_HIDDEN
)

from apps.api.serializers import AuthLoginSerializer
from apps.core.utils import *
from apps.ctf.utils import *

from .consts import *


# Will update security related thing later
# Just implementing basic logics

class BaseView(APIView):
    renderer_classes = [JSONRenderer]


class AdminChallengeList(BaseView):

    def get(self, request):

        if not is_admin(request):
            return Response({'success': False, 'detail': 'You dont have access to this resource'})

        response = self.serialize(request.user)

        if len(response) == 0:
            return Response({'success': False, 'detail': 'Бодлого олдсонгүй'})

        return Response({'success': True, 'data': response})

    def serialize(self, user):
        dynamic_challenges = DynamicChallenge.objects.all()
        standard_challenges = StandardChallenge.objects.all()
        ret = []
        for challenge in standard_challenges:
            ret.append({
                'name': challenge.name,
                'value': challenge.value,
                'description': challenge.description,
                'id': challenge.uuid,
                'state': get_state(challenge.state),
                'category': challenge.category,
                'type': 'стандарт',
            })

        for challenge in dynamic_challenges:
            ret.append({
                'name': challenge.name,
                'value': challenge.value,
                'description': challenge.description,
                'id': challenge.uuid,
                'state': get_state(challenge.state),
                'category': challenge.category,
                'type': 'динамик',

            })
        return ret


class AdminChallenge(BaseView):
    def get(self, request, uuid):
        if not is_admin(request):
            return Response({'success': False, 'detail': ACCESS_DENIED})

        challenge = get_object_or_404(Challenge, uuid=uuid)
        response = self.serialize(challenge)

        return Response({'success': True, 'data': response})

    def post(self, request, uuid):
        if not is_admin(request):
            return Response({'success': False, 'detail': ACCESS_DENIED})

        # Check form security later
        challenge = get_object_or_404(Challenge, uuid=uuid)
        data = request.data.get('data', None)

        # if _type == 'delete':
        #     challenge.delete()
        #     return Response({'success': True, 'detail': SUCCESS_DELETE})

        challenge.name = data['name']
        challenge.category = data['category'].lower()
        challenge.description = data['description']
        challenge.state = get_state(data['state'])
        challenge.value = data['value']

        response = {
            'id': challenge.uuid,
            'name': challenge.name,
            'category': challenge.category,
            'description': challenge.description,
            'state': get_state(challenge.state),
            'value': challenge.value,
            'type': get_type(data['type'])
        }
        challenge.save()
        return Response({'success': True, 'detail': SUCCESS_UPDATED, 'challenge': response})

    def serialize(self, challenge):
        is_dynamic = DynamicChallenge.objects.filter(
            uuid=challenge.uuid).exists()
        hints = Hint.objects.filter(challenge=challenge)
        flags = Flag.objects.filter(challenge=challenge)
        tags = Tag.objects.filter(challenge=challenge)

        ret = {
            'id': challenge.uuid,
            'name': challenge.name,
            'description': challenge.description,
            'value': challenge.value,
            'category': challenge.category,
            'state': get_state(challenge.state),
            'attempts': challenge.max_attempts,
            'type': 'standard',
            'hints': [],
            'flags': [],
            'tags': []
        }

        if is_dynamic:
            ret['decay'] = challenge.dynamicchallenge.decay
            ret['minimum'] = challenge.dynamicchallenge.minimum
            ret['type'] = 'dynamic'

        for hint in hints:
            ret['hints'].append({
                'id': hint.uuid,
                'content': hint.content,
                'cost': hint.cost,
                'state': get_state(hint.state),
            })

        for flag in flags:
            ret['flags'].append({
                'id': flag.uuid,
                'content': flag.content
            })
        for tag in tags:
            ret['tags'].append({
                'id': tag.uuid,
                'content': tag.content
            })

        return ret


class AdminChallengeDelete(BaseView):

    def post(self, request, uuid):
        if not is_admin(request):
            return Response({'success': False, 'detail': ACCESS_DENIED})

        # Check form security later
        challenge = get_object_or_404(Challenge, uuid=uuid)
        challenge.delete()
        return Response({'success': True, 'detail': SUCCESS_DELETED})


class AdminHint(BaseView):

    def post(self, request):
        if not is_admin(request):
            return Response({'success': False, 'detail': ACCESS_DENIED})

        _id = request.data.get('id', None)
        _type = request.data.get('type', None)
        data = request.data.get('data', None)

        if _type == 'add':
            challenge = get_object_or_404(Challenge, uuid=_id)
            hint = Hint.objects.create(
                challenge=challenge,
                content=data['content'],
                cost=data.get('value', ''),
                state=get_state(data.get('state', ''))
            )
            response = {
                'content': hint.content,
                'cost': hint.cost,
                'id': hint.uuid,
                'state': get_state(hint.state)
            }
            hint.save()
            return Response({'success': True, 'detail': SUCCESS_ADD, 'hint': response})

        elif _type == 'delete':
            hint = get_object_or_404(Hint, uuid=_id)
            hint.delete()
            return Response({'success': True, 'detail': SUCCESS_DELETED})


class AdminFlag(BaseView):

    def post(self, request):
        if not is_admin(request):
            return Response({'success': False, 'detail': ACCESS_DENIED})

        _id = request.data.get('id', None)
        _type = request.data.get('type', None)
        data = request.data.get('data', None)

        if _type == 'add':
            challenge = get_object_or_404(Challenge, uuid=_id)
            flag = Flag.objects.create(
                challenge=challenge,
                content=data['content'],
            )
            response = {
                'content': flag.content,
                'id': flag.uuid,
            }
            flag.save()
            return Response({'success': True, 'detail': SUCCESS_ADD, 'flag': response})

        elif _type == 'delete':
            flag = get_object_or_404(Flag, uuid=_id)
            flag.delete()
            return Response({'success': True, 'detail': SUCCESS_DELETED})


class AdminTag(BaseView):

    def post(self, request):
        if not is_admin(request):
            return Response({'success': False, 'detail': ACCESS_DENIED})

        _id = request.data.get('id', None)
        _type = request.data.get('type', None)
        data = request.data.get('data', None)

        if _type == 'add':
            challenge = get_object_or_404(Challenge, uuid=_id)
            tag = Tag.objects.create(
                challenge=challenge,
                content=data['content'],
            )
            response = {
                'content': tag.content,
                'id': tag.uuid,
            }
            tag.save()
            return Response({'success': True, 'detail': SUCCESS_ADD, 'tag': response})

        elif _type == 'delete':
            tag = get_object_or_404(Tag, uuid=_id)
            tag.delete()
            return Response({'success': True, 'detail': SUCCESS_DELETE})


class AdminChallengeAdd(BaseView):

    def post(self, request):
        user = request.user
        data = request.data['data']
        _type = request.data['type']
        if not is_admin(request):
            return Response({'success': False, 'detail': 'You dont have access to this resource'})

        if _type == 'standard':
            challenge = StandardChallenge.objects.create(
                name=data['name'],
                description=data['description'],
                value=data['value'],
                category=data['category'].lower(),
                state=get_state(data['state']),
            )
            flag = Flag.objects.create(
                challenge=challenge,
                content=data['flag']
            )
            response = {
                'id': challenge.uuid,
                'name': challenge.name,
                'category': challenge.category,
                'value': challenge.value,
                'state': get_state(challenge.state),
                'type': 'стандарт',
            }

            challenge.save()
            flag.save()

            return Response({'success': True, 'detail': SUCCESS_ADD, 'challenge': response})

        elif _type == 'dynamic':
            challenge = DynamicChallenge.objects.create(
                name=data['name'],
                description=data['description'],
                value=data['value'],
                category=data['category'].lower(),
                state=get_state(data['state']),
                minimum=data['minimum'],
                decay=data['decay'],
            )

            response = {
                'id': challenge.uuid,
                'name': challenge.name,
                'category': challenge.category,
                'value': challenge.value,
                'state': get_state(challenge.state),
                'type': 'динамик',
            }

            flag = Flag.objects.create(
                challenge=challenge,
                content=data['flag'],
            )

            challenge.save()
            flag.save()

            return Response({'success': True, 'detail': SUCCESS_ADD, 'challenge': response})
        return Response({'success': True})

    def serialize(self, data):
        # Check security later

        name = data.get('name', None)
        description = data.get('description', None)
        value = int(data.get('value', None))
        category = data.get('category', None)
        state = STATE_VISIBLE if data.get(
            'state', None) == 'Ил гаргах' else STATE_HIDDEN
        flag = data.get('flag', None)
        minimum = data.get('minimum', None)
        decay = data.get('decay', None)

        return {
            'name': name,
            'description': description,
            'value': value,
            'category': category,
            'state': state,
            'flag': flag,
            'minimum': minimum,
            'decay': decay,
        }


class AdminConfig(BaseView):

    def get(self, request):
        return Response({'success': True, 'data': 'soemone'})

    def post(self, request):
        user = request.user
        data = request.data['data']

        if not is_admin(request):
            return Response({'success': False, 'detail': ACCESS_DENIED})

        config = Config.objects.filter(key='competition_name').first()
        if config:
            config.value = data['name']
            config.save()
        else:
            Config.objects.create(
                key='competition_name',
                value=data['name']
            ).save()

        config = Config.objects.filter(key='competition_description').first()
        if config:
            config.value = data['description']
            config.save()
        else:
            Config.objects.create(
                key='competition_description',
                value=data['description']
            ).save()

        return Response({'success': True})


class AuthValid(BaseView):

    def post(self, request):
        username = request.data.get('username', None)
        email = request.data.get('email', None)

        # Checking exist or not
        if username:
            count = BaseUser.objects.filter(username=username).count()
            if count > 0:
                return Response({'success': False})
            return Response({'success': True})

        elif email:
            count = BaseUser.objects.filter(email=email).count()
            if count > 0:
                return Response({'success': False})
            return Response({'success': True})
        return Response({'success': True})


class AuthRegister(BaseView):

    def post(self, request):

        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Check valid will update later
        count_username = BaseUser.objects.filter(username=username).count()
        count_email = BaseUser.objects.filter(email=email).count()

        if count_username > 0:
            return Response({'sucess': False, 'detail': 'Нэр бүртгэлтэй байна'})

        if count_email > 0:
            return Response({'success': False, 'detail': 'Емэйл бүртгэлтэй байна'})

        # Creating account
        user = BaseUser.objects.create(
            username=username,
            email=email,
        )

        user.set_password(password)
        user.save()

        return Response({'success': True})


class AuthLogin(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = AuthLoginSerializer


class AuthRefresh(TokenRefreshView):
    pass


class AuthLogout(BaseView):
    permission_classes = (IsAuthenticated,)

    # def post(self, request):
    #     try:
    #         print(request.data)
    #         refresh_token = request.data["refresh_token"]
    #         token = RefreshToken(refresh_token)
    #         token.blacklist()

    #         return Response(status=status.HTTP_205_RESET_CONTENT)
    #     except Exception as e:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({'success': True})


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


class UserSolves(BaseView):

    def get(self, request):
        """
        If user not authenticated then returns []
        """
        user = request.user
        response = []

        if not user.is_authenticated:
            return Response({'success': True, 'data': response})

        solves = Solve.objects.filter(user=user)
        for solve in solves:
            response.append({
                'challenge_id': solve.challenge.uuid
            })
        return Response({'success': True, 'data': response})


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


class UserInfo(BaseView):

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            response = self.serialize(user)

            return Response({'success': True, 'user': response})

        return Response({'success': False})

    def serialize(self, user):
        profile = BaseUserProfile.objects.get(user=user)

        return {
            'username': user.username,
            'type': user.user_type,
            'slug': user.slug,
            'photo': user.photo,
            'fullname': profile.fullname,
        }


class UserProfile(BaseView):
    def get(self, request, slug):
        user = get_object_or_404(BaseUser, slug=slug)

        response = self.serialize(user)

        return Response({'success': True, 'data': response})

    def serialize(self, user):
        profile = BaseUserProfile.objects.get(user=user)
        score = get_score(user)
        value = get_visible_challenges_value()
        res = {
            'username': user.username,
            'type': user.user_type,
            'slug': user.slug,
            'photo': user.photo,
            'fullname': profile.fullname,
        }
        try:
            res['progress'] = int(score / value * 100)
        except Exception as e:
            res['progress'] = 0
        return res


class Scoreboard(BaseView):

    def get(self, request):
        standings = get_standings()
        return Response({'success': True, 'data': standings})


class IsLive(BaseView):

    def get(self, request):
        return Response({'success': True})
