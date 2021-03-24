from apps.ctf.models import Solve
from apps.competition.models import Competition, CompetitionUser
from operator import itemgetter

comp = Competition.objects.all()[0]
participants = CompetitionUser.objects.filter(competition=comp)

users = []
for compU in participants:
    users.append({'user': compU, 'score':Solve.get_score(competition=comp,user=compU.user)})

users = sorted(users, key=itemgetter('score'), reverse=True)
total = len(users)
max_score = users[0]['score']

# From ctftime rating formula
for _ in range(0, total):
    points_coef = users[_]['score'] / max_score
    place_coef = 1 / (_ + 1)
    rating = ((points_coef + place_coef) * comp.weight) / (1 / (1 + _ // total))
    users[_]['user'].score = users[_]['score']
    users[_]['user'].rating = rating
    users[_]['user'].save()