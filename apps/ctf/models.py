from django.db import models
from apps.core.models import (
    BaseModel,
    BaseUserProfile,
    BaseUser,
)
from math import ceil
from apps.ctf.consts import *
from datetime import datetime, timedelta
from django.utils import timezone


class Challenge(BaseModel):
    flags = models.ForeignKey(
        'Flag', verbose_name="Flag", related_name="challenge_flag", on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ForeignKey('Tag', related_name="challenge_tag",
                             on_delete=models.CASCADE, null=True, blank=True)
    hints = models.ForeignKey(
        'Hint', related_name="challenge_hint", on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField("Name", max_length=30, unique=True)
    description = models.TextField("Description")
    value = models.PositiveIntegerField("Value", default=1000, null=True)

    category = models.CharField(
        "Category", max_length=100, null=True)
    state = models.CharField(
        "State", choices=STATE_CHOICES, max_length=100, default=STATE_VISIBLE)
    max_attempts = models.PositiveIntegerField("Max attempts", default=0)

    class Meta:
        verbose_name = "Challenge"

    def __str__(self):
        return f"{self.name} | {self.category} | {self.uuid}"

    @classmethod
    def attempt(cls, challenge, request):
        data = request.data
        submission = data['submission'].strip()
        flags = Flag.objects.filter(challenge=challenge)
        for flag in flags:
            if Flag.compare(flag, submission):
                return True, "Зөв байна"
            else:
                return False, "Буруу байна"

    @classmethod
    def solve(cls, user, challenge, request):
        data = request.data
        submission = data['submission'].strip()

        Solve.objects.create(
            user=user,
            challenge=challenge,
            submission=submission
        ).save()


class DynamicChallenge(Challenge):
    initial = models.PositiveIntegerField(
        "Initial value", default=1000, null=True)
    minimum = models.PositiveIntegerField(
        "Minimum value", default=100, null=True)
    decay = models.PositiveIntegerField("Decay", default=25, null=True)

    class Meta:
        verbose_name = 'DynamicChallenge'

    def save(self, *args, **kwargs):
        self.initial = self.value
        return super(DynamicChallenge, self).save(*args, **kwargs)

    @classmethod
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

    @classmethod
    def solve(cls, user, challenge, request):
        super().solve(user, challenge, request)

        DynamicChallenge.calculate_value(challenge)


class StandardChallenge(Challenge):

    class Meta:
        verbose_name = 'StandardChallenge'


class Flag(BaseModel):
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE)
    content = models.CharField('Content', max_length=100)

    class Meta:
        verbose_name = "Flag"

    def __str__(self):
        return f"Flag: {self.content} for {self.challenge.name}"

    # From CTFd
    @staticmethod
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


class Hint(BaseModel):
    REQUIRED_FIELDS = ['challenge']

    challenge = models.ForeignKey(
        Challenge, verbose_name="Challenge", on_delete=models.CASCADE)
    content = models.CharField("Зөвлөгөө", max_length=100)
    state = models.CharField("State", choices=STATE_CHOICES,
                             max_length=100, default=STATE_VISIBLE)

    cost = models.PositiveIntegerField("Татвар", default=0)

    class Meta:
        verbose_name = "Hint"

    def __str__(self):
        return f'{self.challenge.name} | {self.content}'


class Config(BaseModel):
    key = models.CharField(max_length=200, db_index=True)
    value = models.CharField(max_length=200, db_index=True)

    class Meta:
        verbose_name = 'Config'

    def __str__(self):
        return f'{self.key} | {self.value}'
