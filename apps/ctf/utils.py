from .consts import *
from .models import *
from apps.core.consts import *
from django.db.models import Sum
from operator import itemgetter

CHALLENGE_CLASSES = {"standard": StandardChallenge,
                     "dynamic": DynamicChallenge}


def get_state(data):
    if data == STATE_VISIBLE_MN:
        return STATE_VISIBLE
    elif data == STATE_HIDDEN_MN:
        return STATE_HIDDEN
    elif data == STATE_VISIBLE:
        return STATE_VISIBLE_MN
    elif data == STATE_HIDDEN:
        return STATE_HIDDEN_MN


def get_type(data):
    if data == TYPE_DYNAMIC_MN:
        return TYPE_DYNAMIC
    elif data == TYPE_STANDARD_MN:
        return TYPE_STANDARD
    elif data == TYPE_DYNAMIC:
        return TYPE_DYNAMIC_MN
    elif data == TYPE_STANDARD:
        return TYPE_STANDARD_MN


def get_standings():
    res = []
    for user in BaseUser.objects.filter(user_type=USER_TYPE_NORMAL):
        score = get_score(user)
        if not score:
            score = 0
        res.append({
            'username': user.username,
            'score': score
        })
    return sorted(res, key=itemgetter('score'), reverse=True)


def get_score(user):
    result = Solve.objects.filter(user=user, challenge__state__contains=STATE_VISIBLE).aggregate(
        Sum('challenge__value'))['challenge__value__sum']

    if not result:
        result = 0
    return result


def get_chall(challenge_id):
    chall = StandardChallenge.objects.filter(uuid=challenge_id).first()
    if not chall:
        return DynamicChallenge.objects.filter(uuid=challenge_id).first()
    return chall


def get_visible_challenges_value():
    result = Challenge.objects.filter(state=STATE_VISIBLE).aggregate(
        Sum('value'))['value__sum']

    if not result:
        result = 0
    return result
