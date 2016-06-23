from django.core import serializers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from Course.models import Course
from .models import Lane

@login_required
def index(request, course_short_title):
    """index renders a simple html page and adds the react frontend code."""

    # Course and lanes are directly passed via javascript variables to the
    # frontend code, since they are never changed by the app. This speeds up the
    # rendering, since we don't have make seperate requests for the information.
    course = Course.get_or_raise_404(course_short_title)
    lanes = serializers.serialize("json", Lane.objects.all().filter(hidden=False).order_by('order'), fields=('name'))

    return render(
        request, 'Feedback/index.html',
        {
            'course': course,
            'lanes': lanes,
        }
    )