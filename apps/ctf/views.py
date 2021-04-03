from django.db.models import F, Count
from datetime import datetime, timezone
from rest_framework.response import Response
from apps.api.views import BaseView
from .consts import *
from .utils import *
from .models import (
    Challenge,
)
from apps.core.consts import SOMETHING_WRONG
from apps.competition.consts import *
from apps.competition.models import (
    Competition,
    CompetitionUser
)

from apps.core.utils import (
    convert_to_localtime,
    td_format,
    calculate_percentage
)


class ChallengeList(BaseView):
    """
    Endpoint of public challenges
    """

    def get(self, request):
        challenges = Challenge.objects.filter(
            state=STATE_VISIBLE, competition=None).values('uuid', 'name', 'category', author=F('user__username'))
        return Response({'success': True, 'data': list(challenges)})


class ChallengeView(BaseView):

    def get(self, request, uuid):
        chall = Challenge.objects.filter(uuid=uuid).first()

        if not chall:
            return Response({'success': False})

        resp = self.serialize(chall=chall, req=request)

        return Response({'success': True, 'data': resp})

    def serialize(self, chall, req):
        return {
            'author': {
                'username': chall.user.username,
                'slug': chall.user.slug
            },
            'name': chall.name,
            'value': chall.value,
            'description': chall.description,
            'id': chall.uuid,
        }


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


class ChallengeRequest(BaseView):

    def post(self, request):
        user = request.user
        data = request.data['data']

        if not user.is_authenticated:
            return Response({'success': False, 'detail': AUTHENTICATION_REQUIRED})

        # If user requested more than 5 challenge then one time
        # We don't accept new challenge until old ones
        if Challenge.objects.filter(user=user, state=STATE_LOCKED).count() > 5:
            return Response({'success': False, 'detail': 'Таны өмнөх бодлогууд шалгагдаж дуусаагүй байна'})

        # Adding challenge
        chall = DynamicChallenge.objects.create(
            user=user,
            name=data['name'],
            description=data['description'],
            category=data['category'].lower(),
            solution=data['solution'],
            state=STATE_LOCKED,
        )

        Flag.objects.create(
            content=data['flag'],
            challenge=chall
        )

        return Response({'success': True, 'detail': SUCCESS_ADD})

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


class ChallengesSolves(BaseView):
    def get(self, request):
        challenges = Challenge.objects.filter(
            state=STATE_VISIBLE, competition=None)

        response = self.serialize(challenges)

        return Response({'success': True, 'data': response})

    def serialize(self, challenges):
        ret = []
        for challenge in challenges:
            solves = Solve.objects.filter(challenge=challenge).count()
            ret.append({
                'id': challenge.uuid,
                'solves': solves
            })
        return ret


class Scoreboard(BaseView):

    def get(self, request):
        response = self.serialize()

        return Response({'success': True, 'data': response})

    def serialize(self):
        res = []

        total_value = get_visible_challenges_value()
        fblood = self.get_firstblood()
        ind = 1
        for user in BaseUser.objects.filter(user_type=USER_TYPE_NORMAL):
            total_score, total_solved_challs = self.get_public_challs(
                user=user)

            # If user total_score <= 0 then we will skip
            if not total_score:
                continue

            total_rating, total_win = self.get_contest_rating(user=user)

            first_blood = 0
            if user.username in fblood:
                first_blood = fblood[user.username]

            res.append({
                'username': user.username,
                'slug': user.slug,
                'total_solved_challs': total_solved_challs,
                'total_win': total_win,
                'total_rating': total_rating,
                'progress': calculate_percentage(total_score, total_value),
                'fblood': first_blood,
            })
        users = sorted(res, key=itemgetter('total_rating'), reverse=True)
        for user in users:
            user['place'] = ind
            ind += 1
        return users

    def get_public_challs(self, user):
        solved_challs = Solve.objects.filter(
            user=user, challenge__state__contains=STATE_VISIBLE, challenge__competition=None)
        total_score = solved_challs.aggregate(models.Sum('challenge__value'))[
            'challenge__value__sum']
        total_solved_challs = solved_challs.count()

        if not total_solved_challs:
            total_solved_challs = 0
        return total_score, total_solved_challs

    def get_contest_rating(self, user):
        total_rating, total_win = 0, 0
        for compUser in CompetitionUser.objects.filter(user=user, competition__status__contains=COMPETITION_ARCHIVE):

            total_rating += compUser.rating
            total_win += 1 if compUser.place == 1 else 0

        return round(total_rating, 2), total_win

    def get_firstblood(self):
        total = {}

        for chall in Challenge.objects.filter(state=STATE_VISIBLE, competition=None):
            solve = Solve.objects.filter(challenge=chall).first()
            if not solve:
                continue
            if solve.user.username not in total:
                total[solve.user.username] = 1
            else:
                total[solve.user.username] += 1
        return total


class Writeups(BaseView):

    def get(self, request, uuid):
        user = request.user

        chall = Challenge.objects.filter(uuid=uuid).first()

        if not chall:
            return Response({'success': False, 'detail': SOMETHING_WRONG})

        status, message = self.check_valid(user=user, challenge=chall)

        if not status:
            return Response({'success': False, 'detail': message})

        response = self.serialize(user=user, challenge=chall)

        return Response({'success': True, 'data': response, 'challenge': {'name': chall.name, 'id': chall.uuid}})

    def check_valid(self, user, challenge):
        if challenge.competition and challenge.competition.status == COMPETITION_ARCHIVE and challenge.state == STATE_VISIBLE:
            return True, SUCCESS
        elif not user.is_authenticated:
            return False, AUTHENTICATION_REQUIRED

        if Solve.objects.filter(user=user, challenge=challenge).exists() or challenge.user.username == user.username:
            return True, SUCCESS

        return False, SOMETHING_WRONG

    def serialize(self, user, challenge):
        res, writeups = [], []
        for _ in Writeup.objects.filter(challenge=challenge):
            like = WriteupUser.objects.filter(
                writeup=_, reaction=REACTION_LIKE).count()
            dislike = WriteupUser.objects.filter(
                writeup=_, reaction=REACTION_DISLIKE).count()
            power = like - dislike
            writeups.append({'id': _.uuid, 'power': power})

        for _ in writeups:
            writeup = Writeup.objects.get(uuid=_['id'])
            res.append({
                'power': _['power'],
                'id': writeup.uuid,
                'name': writeup.challenge.name,
                'created': convert_to_localtime(writeup.created_date).split(' ')[0],
                'content': writeup.content,
                'status': False,
                'author': {
                    'username': writeup.author.username,
                    'slug': writeup.author.slug,
                }
            })
            if user.is_authenticated:
                userWriteup = WriteupUser.objects.filter(
                    author=user, writeup=writeup).first()
                if userWriteup:
                    res[len(res)-1]['status'] = userWriteup.reaction

        return res

    def post(self, request):
        data = request.data
        user = request.user

        action = data['action']

        if not user.is_authenticated:
            return Response({'success': False, 'detail': AUTHENTICATION_REQUIRED})

        writeup = Writeup.objects.get(uuid=data['id'])
        writeUser = WriteupUser.objects.filter(
            author=request.user, writeup=writeup).first()

        if not writeUser:
            WriteupUser.objects.create(
                writeup=writeup,
                author=user,
                reaction=action
            )
            return Response({'success': True})

        if action == REACTION_DISLIKE:
            if writeUser.reaction == REACTION_DISLIKE:
                writeUser.delete()
                return Response({'success': True})
            elif writeUser.reaction == REACTION_LIKE:
                writeUser.reaction = REACTION_DISLIKE

        elif action == 'like':
            if writeUser.reaction == REACTION_LIKE:
                writeUser.delete()
                return Response({'success': True})

            elif writeUser.reaction == REACTION_DISLIKE:
                writeUser.reaction = REACTION_LIKE

        writeUser.save()

        return Response({'success': True})


class WriteupView(BaseView):
    def post(self, request):
        status, message = self.check_valid(request)

        if not status:
            return Response({'success': False, 'detail': message})

        if request.data['action'] == 'add':
            response = self.add(request)

            return Response({'success': True, 'data': response})

        return Response({'success': False})

    def add(self, req):
        user = req.user
        data = req.data

        chall = Challenge.objects.get(uuid=data['id'])

        writeup = Writeup.objects.create(
            author=user,
            challenge=chall,
            content=data['data'],
        )
        return {
            'power': 0,
            'id': writeup.uuid,
            'name': writeup.challenge.name,
            'created': convert_to_localtime(writeup.created_date).split(' ')[0],
            'content': writeup.content,
            'status': False,
            'author': {
                'username': writeup.author.username,
                'slug': writeup.author.slug,
            }
        }

    def check_valid(self, req):
        user = req.user
        data = req.data

        if not user.is_authenticated:
            return False, AUTHENTICATION_REQUIRED

        chall = Challenge.objects.filter(uuid=data['id']).first()

        if not chall:
            return False, NOT_FOUND

        if chall.competition and chall.competition.status == COMPETITION_ARCHIVE:
            return True, SUCCESS

        solve = Solve.objects.filter(user=user, challenge=chall).first()

        if solve or chall.user.username == user.username:
            return True, SUCCESS

        return False, SOMETHING_WRONG


class TodayTop(BaseView):
    def get(self, request):
        top = Solve.objects.filter(created_date__gte=timezone.localtime().replace(hour=0, minute=0, second=0)).annotate(
            player=Count('user')).order_by('-player').select_related('user').first()
        if not top:
            return Response({
                'success': False
            })

        return Response({
            'success': True,
            'data': {
                'user': {
                    'username': top.user.username,
                    'slug': top.user.slug,
                    'img': 'https://avatar.ctflearn.com/aae0b980cce0b34fcfed8908bba52905.png',
                },
                'total_solved': Solve.get_total_solved(user=top.user),
                'total_score': Solve.get_score(user=top.user),
                'total_comp': CompetitionUser.objects.filter(user=top.user).count()
            }
        })
