from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.http import Http404
from Stack.models import Stack, StackChallengeRelation

@login_required()
def stack(request, course_short_title=None):
    data = create_context_stack(request, course_short_title)
    return render_to_response('stack.html', data, context_instance=RequestContext(request))

def index(request):
    return render(request, 'badges.html', {})

def badges(request, course_short_title=None):
    return render(request, 'badges.html', {})
