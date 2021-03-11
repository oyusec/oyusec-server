from django.shortcuts import render
from django.views import View

class HomeView(View):
    context = {'title': 'API хуудас - OyuSec', }

    def get(self, request, *args, **kwargs):
        return render(request, 'Index.html', self.context)

