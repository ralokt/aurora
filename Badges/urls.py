from django.conf.urls import patterns, url

import Badges.views

urlpatterns = patterns('',
                        url(r'^$', Badges.views.badges, name='home'),
                        )