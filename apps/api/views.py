from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


from django.shortcuts import get_object_or_404

from apps.core.models import (
    BaseUser,
    BaseUserProfile
)

from apps.ctf.models import (
    StandardChallenge,
    DynamicChallenge,
    Submission,
    Challenge,
    Config,
    Solve,
    Flag,
    Hint,
    Tag,
)


from apps.core.utils import *


class BaseView(APIView):
    renderer_classes = [JSONRenderer]


class IsLive(BaseView):

    def get(self, request):
        return Response({'success': True})
