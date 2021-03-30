from django.db import models
from apps.core.models import (
    BaseModel,
    BaseUserProfile,
    BaseUser,
)

from math import ceil
from datetime import datetime, timedelta
from django.utils import timezone
from .consts import *


def get_admin():
    return BaseUser.objects.filter(username='admin').first()


class Challenge(BaseModel):
    REQUIRED_FIELDS = ['base_user']

    name = models.CharField("Name", max_length=30, unique=True)
    description = models.TextField("Description")
    value = models.PositiveIntegerField("Value", default=1000, null=True)
    user = models.ForeignKey(
        BaseUser, verbose_name='Author', on_delete=models.CASCADE, null=True, default=get_admin)

    category = models.CharField(
        "Category", max_length=100, null=True)
    state = models.CharField(
        "State", choices=STATE_CHOICES, max_length=100, default=STATE_VISIBLE)
    max_attempts = models.PositiveIntegerField("Max attempts", default=0)
    competition = models.ForeignKey(
        'competition.Competition',  on_delete=models.CASCADE, null=True, blank=True)
    solution = models.TextField("Solution", default='')

    class Meta:
        verbose_name = "Challenge"

    def __str__(self):
        return f"{self.name} | {self.category} | {self.competition}"

    @classmethod
    def check_valid(cls, user, challenge, request):
        if challenge.user.username == user.username:
            return False, AUTHOR_CHALLENGE
        if Solve.objects.filter(user=user, challenge=challenge).exists():
            return False, ALREADY_SOLVED
        return True, NOT_SOLVED

    @ classmethod
    def attempt(cls, challenge, request):
        data = request.data
        submission = data['submission'].strip()
        flags = Flag.objects.filter(challenge=challenge)

        for flag in flags:
            if Flag.compare(flag, submission):
                return True, SUBMISSION_CORRECT_MN
            else:
                return False, SUBMISSION_WRONG_MN

        # This will happen if challenge have no flag
        # So returning false
        return False, SUBMISSION_WRONG_MN

    @ classmethod
    def solve(cls, user, challenge, request):
        data = request.data
        submission = data['submission'].strip()

        Solve.objects.create(
            user=user,
            challenge=challenge,
            submission=submission
        )


class DynamicChallenge(Challenge):
    initial = models.PositiveIntegerField(
        "Initial value", default=1000, null=True)
    minimum = models.PositiveIntegerField(
        "Minimum value", default=100, null=True)
    decay = models.PositiveIntegerField("Decay", default=25, null=True)

    class Meta:
        verbose_name = 'Dynamic challenge'

    def save(self, *args, **kwargs):
        self.initial = self.value
        return super(DynamicChallenge, self).save(*args, **kwargs)

    @ classmethod
    def calculate_value(cls, challenge):
        solve_count = Solve.objects.filter(challenge=challenge).count()

        if solve_count != 0:
            solve_count -= 1

        value = (
            ((challenge.minimum - challenge.initial) / (challenge.decay ** 2))
            * (solve_count ** 2)
        ) + challenge.initial
        value = ceil(value)

        if value < challenge.minimum:
            value = challenge.minimum

        challenge.value = value
        challenge.save()

    @ classmethod
    def solve(cls, user, challenge, request):
        super().solve(user, challenge, request)

        DynamicChallenge.calculate_value(challenge)


class StandardChallenge(Challenge):

    class Meta:
        verbose_name = 'Standard challenge'


class Flag(BaseModel):
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE)
    content = models.CharField('Content', max_length=100)

    class Meta:
        verbose_name = "Flag"

    def __str__(self):
        return f"Flag: {self.content} for {self.challenge.name}"

    # From CTFd
    @ staticmethod
    def compare(flag, provided):
        flag = flag.content

        if len(flag) != len(provided):
            return False

        result = 0

        for x, y in zip(flag, provided):
            result |= ord(x) ^ ord(y)
        return result == 0


class Tag(BaseModel):
    REQUIRED_FIELDS = ["challenge"]
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    content = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Tag"

    def __str__(self):
        return f"{self.challenge.name} | {self.content}"


class Submission(BaseModel):
    REQUIRED_FIELDS = ["base_user", "challenge"]

    user = models.ForeignKey(
        BaseUser, verbose_name="User", on_delete=models.CASCADE)
    challenge = models.ForeignKey(
        Challenge, verbose_name="Challenge", on_delete=models.CASCADE)
    submission = models.TextField("Submission")

    class Meta:
        verbose_name = "Submission"

    def __str__(self):
        return f'{self.user.username} | {self.challenge.name} | {self.submission}'


class Solve(Submission):

    class Meta:
        verbose_name = "Solve"

    def __str__(self):
        return f"{self.user.username} | {self.challenge.name}"

    @ classmethod
    def get_score(cls, user, competition):
        result = Solve.objects.filter(user=user, challenge__state__contains=STATE_VISIBLE, challenge__competition=competition).aggregate(
            models.Sum('challenge__value'))['challenge__value__sum']

        if not result:
            result = 0
        return result

    @ classmethod
    def get_total_solved(cls, user, competition=None):
        result = Solve.objects.filter(
            user=user, challenge__state__contains=STATE_VISIBLE, challenge__competition=competition).count()
        return result


class Hint(BaseModel):
    REQUIRED_FIELDS = ['challenge']

    challenge = models.ForeignKey(
        Challenge, verbose_name="Challenge", on_delete=models.CASCADE)
    content = models.CharField("Зөвлөгөө", max_length=100)
    state = models.CharField("State", choices=STATE_CHOICES,
                             max_length=100, default=STATE_VISIBLE)
    cost = models.PositiveIntegerField("Cost", default=0)

    class Meta:
        verbose_name = "Hint"

    def __str__(self):
        return f'{self.challenge.name} | {self.content}'
