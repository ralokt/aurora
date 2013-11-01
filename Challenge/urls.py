from django.conf.urls import patterns, url
from Challenge import views as challenge_views
from django.http import HttpResponsePermanentRedirect

urlpatterns = patterns('',
    url(r'^challenges/$', 'Challenge.views.challenges_overview'),
    url(r'^challenges/stack$', 'Challenge.views.challenges_stack'),
    url(r'^challenges/challenge$', 'Challenge.views.challenge_detail'),
    url(r'^challenges/submit$', 'Challenge.views.submit_challenge'),
    url(r'^challenges/autosave/$', 'Elaboration.views.save_elaboration'),
)