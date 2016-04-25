
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from Stack.models import Stack, StackChallengeRelation
#from Course.models import Course, CourseUserRelation


badges = ['badgeEvaluatedPoints', 'badgeHandInPoints']

#-badge primary key consists of name, user and course
class Badge(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey('AuroraUser.AuroraUser')
    course = models.ForeignKey('Course.Course')
    progress = models.IntegerField()

#-change progress for one badge according to its rules
def updateBadgeProgress(data, badgename, user, course, progress=0):
 #-progress = 0


    #-b = data['stacks'][0]['evaluated_points_earned_total ']
   #-print(data)

    #-for v in data['stacks']:
    #-    if data['course_title'] == "Human Computer Interaction":
     #-       b = data['stacks']['evaluated_points_earned_total']
      #-      print(b)
        #-1. !!! sumbadgepoints holen, vergleichen, percent berechnen und neuen progress anfuegen (unten im try)
        #-zweites array element = course, check schreiben ob hci/gsi
        #_________________________


       #- x = Stack.Stack.objects.get(user = user)
       #- print(x)
       #- print(Stack.Stack.evaluated_points_earned_total(Stack, user = user))

        #-progressPercent = progress
    #dunno ob das uncomm. oder nicht!!!!!!!!!!!
    #elif badgename == 'badgeHandInPoints':
      #  progress = 42

     #   course = Course.get_or_raise_404(short_title=course_short_title)

    try:
        b = Badge.objects.get(name = badgename, user = user, course = course)
        b.progress = progress
        b.save()
        print(b.progress)


    except Badge.DoesNotExist:
        newb = Badge(name=badgename, user=user, course=course, progress=progress)
        newb.save()

# check progress for one badge
def badgeProgress(badgename, user, course):
    try:
        b = Badge.objects.get(name = badgename, user = user, course = course)
        if b:
            return b.progress
        else:
            return 0
    except Badge.DoesNotExist:
        return 0

# check progress for all badges
def all_badge_progresses(user, course):
    progresses = []
    for badge in badges:
        progresses.append((badge, badgeProgress(badge,user,course)))

    return progresses