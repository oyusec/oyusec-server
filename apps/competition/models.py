from django.db import models
from django.template.defaultfilters import slugify
from apps.core.models import (
    BaseModel,
    BaseUser,
)
from .consts import *


class Competition(BaseModel):
    name = models.CharField('Name', max_length=100, default='OyuSec')
    description = models.TextField('Description', default='CTF')
    status = models.CharField('Status', choices=COMPETITION_STATUS_CHOICES,
                              max_length=100, default=COMPETITION_COMING)
    slug = models.SlugField(null=False, unique=True)
    photo = models.URLField(
        null=True, blank=True, default="https://github.com/OyuTech/Utils/blob/main/oyusec/oyusec.png")
    rule = models.TextField(default='')
    prize = models.TextField()
    participants = models.ManyToManyField(
        BaseUser,  through='CompetitionUser')
    location = models.CharField('Location', max_length=100, default='онлайн')
    enrollment = models.CharField(
        'Enrollment', max_length=100, default=ENROLLMENT_SOLO, choices=ENROLLMENT_CHOICES)
    start_date = models.DateTimeField(auto_now_add=False, blank=True)
    end_date = models.DateTimeField(auto_now_add=False, blank=True)

    class Meta:
        verbose_name = 'Competition'

    def __str__(self):
        return f'{self.name} | {self.status}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Competition, self).save(*args, **kwargs)


class CompetitionUser(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    score = models.PositiveIntegerField('Score', default=0)

    class Meta:
        verbose_name = 'Competition User'

    def __str__(self):
        return f'{self.user.username} | {self.competition.name}'
