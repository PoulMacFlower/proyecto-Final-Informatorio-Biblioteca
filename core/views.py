from django.views.generic import View
from django.shortcuts import render



class HomeView(View):
    def get(self, request, *args, **kwargs):
        context={
            
        }
        return render(request, 'home.html',context)
    
def handling_404(request, exeception):
    return render (request, '404/404.html', {})  