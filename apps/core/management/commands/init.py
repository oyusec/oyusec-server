from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from datetime import datetime
from apps.core.models import BaseUser
from apps.ctf.models import (
    StandardChallenge,
    DynamicChallenge,
    Challenge,
    Solve,
    Flag,
)
from apps.competition.models import (
    Competition,
    CompetitionUser
)
from apps.core.consts import *
from apps.ctf.consts import *
from apps.competition.consts import *

# Misc
import random


class Command(BaseCommand):
    help = 'Initialize default values'

    def handle(self, *args, **kwargs):
        self.create_admin()
        self.create_users()
        self.create_competitions()
        self.create_challenges()
        self.create_flags()
        self.create_solves()

    def create_admin(self):
        BaseUser.objects.create_superuser(
            username=FAKE_ADMIN,
            email=FAKE_ADMIN_EMAIL,
            password=FAKE_PASSWORD,
        )

        self.stdout.write("[+] Created admin")

    def create_users(self):
        user = BaseUser.objects.create(
            username=FAKE_GUEST_USERNAME,
            email=FAKE_GUEST_EMAIL
        )
        user.set_password(FAKE_PASSWORD)
        user.save()

        for _ in range(20):
            user = BaseUser.objects.create(
                username=f'{FAKE_USER_USERNAME}{_}',
                email=f'{FAKE_USER_USERNAME}{_}@zxc.zxc',
            )
            user.set_password(FAKE_PASSWORD)
            user.save()

        self.stdout.write("[+] Created users")

    def create_competitions(self):

        for _ in range(10):
            rand_date = random.randint(1, 29)
            rand_hour = random.randint(0, 23)
            rand_img = random.choice(FAKE_IMAGES)
            rand_status = random.choice(FAKE_STATUS)
            rand_location = random.choice(FAKE_COMPETITION_LOCATIONS)

            Competition.objects.create(
                name=f'{FAKE_COMPETITION_NAME} #{_}',
                description=FAKE_COMPETITION_DESCRIPTION,
                prize=FAKE_COMPETITION_PRIZE,
                rule=FAKE_COMPETITION_RULE,
                location=rand_location,
                enrollment=random.choice([ENROLLMENT_SOLO, ENROLLMENT_TEAM]),
                start_date=make_aware(
                    datetime(2021, 3, rand_date, rand_hour, 0)),
                end_date=make_aware(
                    datetime(2021, 3, rand_date + 1, rand_hour, 0)),
                photo=rand_img,
                status=rand_status,
            )

    def create_challenges(self):

        # Public challenges
        for _ in range(30):
            DynamicChallenge.objects.create(
                name=f'{FAKE_CHALLENGE_NAME} {_}',
                category=random.choice(FAKE_CHALLENGE_CATEGORIES),
                description=FAKE_CHALLENGE_DESCRIPTION,
            )
        # Competition challenges
        for _ in range(40):
            DynamicChallenge.objects.create(
                name=f'{FAKE_COMPETITION_CHALLENGE_NAME} {_}',
                category=random.choice(FAKE_CHALLENGE_CATEGORIES),
                description=FAKE_CHALLENGE_DESCRIPTION,
                competition=random.choice(Competition.objects.all()),
            )

        self.stdout.write("[+] Created challenges")

    def create_flags(self):
        # Makes all flag same
        for _ in Challenge.objects.all():
            Flag.objects.create(content=FAKE_FLAG, challenge=_)

        self.stdout.write('[+] Created flags')

    def create_solves(self):
        self.stdout.write('[+] Creating solves')

        for user in BaseUser.objects.filter(user_type=USER_TYPE_NORMAL):

            challenges_id = list(Challenge.objects.filter(
                state=STATE_VISIBLE).values_list('uuid', flat=True))
            solves_challenges = random.sample(
                challenges_id, min(len(challenges_id), 5))
            challenges = Challenge.objects.filter(uuid__in=solves_challenges)

            for challenge in challenges:
                Solve.objects.create(
                    user=user,
                    challenge=challenge,
                    submission=FAKE_FLAG
                )
                if challenge.competition:
                    CompetitionUser.objects.create(
                        user=user,
                        competition=challenge.competition
                    )

        self.stdout.write('[+] Calculating dynamic values')

        for challenge in DynamicChallenge.objects.filter(state=STATE_VISIBLE):
            challenge.calculate_value(challenge)
