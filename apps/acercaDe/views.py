from django.shortcuts import render
from django.views.generic import View


class AllAboutView(View):
    def get(self, request, *args, **kwargs):
        context = {
            
        }
        return render(request, 'about/about.html', context)
