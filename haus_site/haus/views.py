from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader

# Create your views here.


@login_required
def home(request):
    context = RequestContext(request, {
        'user': request.user
    })
    template = loader.get_template('haus/dataview.html')
    return HttpResponse(template.render(context))
