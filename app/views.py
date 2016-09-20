"""
Definition of views.
"""

import sentiment
import json
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
from xml.sax.saxutils import unescape
from django.shortcuts import render

def analyze(request):
    response = sentiment.analyze(request.body)

    #return HttpResponse(unescape(json.dumps(response)), content_type='application/json')
    return render(request, 'app/indexpartial-vert.html', response, content_type='text/html')

def home(request):
    response = {}
    text = ''
    if request.method == 'POST':
        text = request.POST['text']
        response = sentiment.analyze(text)

    return render(request, 'app/index.html', response)

def mirror(request):
    return HttpResponse(request.body, content_type='text/html')

#def contact(request):
#    """Renders the contact page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/contact.html',
#        context_instance = RequestContext(request,
#        {
#            'title':'Contact',
#            'message':'Your contact page.',
#            'year':datetime.now().year,
#        })
#    )

#def about(request):
#    """Renders the about page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/about.html',
#        context_instance = RequestContext(request,
#        {
#            'title':'About',
#            'message':'Your application description page.',
#            'year':datetime.now().year,
#        })
#    )
