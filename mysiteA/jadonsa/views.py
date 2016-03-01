from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from django.template import loader


# Create your views here.
def index(request):
	return HttpResponse("Hello, world.")

class Jadonsa(generic.ListView):
    template_name = 'jadonsa/jjj.html'
    context_object_name = None

    def get_queryset(self):
        return {}



def test(request):
    template = loader.get_template('jadonsa/test.html')
    return HttpResponse(template.render(request))
