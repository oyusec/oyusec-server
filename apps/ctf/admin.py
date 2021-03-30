from django.contrib import admin
from .models import *

admin.site.register(StandardChallenge)
admin.site.register(DynamicChallenge)
admin.site.register(Submission)
admin.site.register(Solve)
admin.site.register(Hint)
admin.site.register(Flag)
admin.site.register(Tag)
