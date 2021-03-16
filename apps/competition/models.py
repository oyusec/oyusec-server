from django.db import models
from apps.core.models import (
    BaseModel,
    BaseUser,
)
from .consts import *


class Competition(BaseModel):
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description')
    status = models.CharField('Status', choices=COMPETITION_STATUS_CHOICES,
                              max_length=100, default=COMPETITION_UPCOMING)
    slug = models.SlugField(null=False, unique=True)
    photo = models.URLField(
        null=True, blank=True, default="https://github.com/OyuTech/Utils/blob/main/oyusec/oyusec.png")
    participants = models.ManyToManyField(
        BaseUser,  through='CompetitionUser')

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
