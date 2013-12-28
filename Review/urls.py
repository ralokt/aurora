from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^challenges/challenge_review/$', 'Review.views.review_page'),
    url(r'^challenges/get_challenge_review/$', 'Review.views.review'),
    url(r'^challenges/challenge_review/review_answer/$', 'Review.views.review_answer'),
    url(r'^challenges/received_challenge_reviews/$', 'Review.views.received_challenge_reviews_page'),
    url(r'^challenges/get_received_challenge_reviews/$', 'Review.views.received_challenge_reviews'),
    url(r'^review/escalate/$', 'Review.views.review_escalate'),
)