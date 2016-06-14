from django.db import models
from Stack.models import Stack, StackChallengeRelation, Chapter
from pprint import pprint
from django.http import HttpResponse

badges = [('badge_evaluated_points', 40), ('badge_handed_in_points', 60), ('badge_all_chapter', 5)]

# badge primary key consists of name, user and course
class Badge(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey('AuroraUser.AuroraUser')
    course = models.ForeignKey('Course.Course')
    progress = models.IntegerField()

# update badge progress of all badges in DB
def update_badge_progresses(data,user,course):
    for b in badges:
        update_badge_progress(data,b,user,course)

# change progress for one badge according to its rules
def update_badge_progress(data, badge, user, course, progress=0):

    badgename = badge[0]

    # conditions for main badge evaluated Points
    if badgename == 'badge_evaluated_points':

        ptsUpdate = next((item["evaluated_points_earned_total"] for item in data["stacks"] if
                         item["course_title"] == str(course)), None)

        progress += ptsUpdate

    # conditions for main badge showing handed in points
    if badgename == 'badge_handed_in_points':

        courseFiltered = next((item["course_stacks"] for item in data["stacks"] if
                         item["course_title"] == str(course)), None)

        started = [x for x in courseFiltered if x["is_submitted"] is True]

        progress = sum(x["points_available"] for x in started)

    # conditions for main badge chapter task: at least one task from all chapters
    if badgename == 'badge_all_chapter':
        chapterChecker = next((item["course_stacks"] for item in data["stacks"] if item["course_title"] == str(course)),
                              None)

        chapterList = set()

        for c in Stack.objects.all().filter(course = course):
            chapterList.add(c.chapter)

        if chapterChecker is None:
            progress += 0
        if chapterList is None:
            maximum = 0
        else:
            maximum = len(chapterList)
            badges[2] = ("badge_all_chapter", maximum)
            progress += len([x for x in chapterChecker if x["is_submitted"] is True])

    try:
        b = Badge.objects.get(name=badgename, user=user, course=course)
        b.progress = progress
        b.save()

    except Badge.DoesNotExist:
        newb = Badge(name=badgename, user=user, course=course, progress=progress)

        newb.save()

# read progress for one badge from DB
def badge_progress(badge, user, course):
    try:
        b = Badge.objects.get(name=badge[0], user=user, course=course)
        if b:

            return b.progress
        else:
            return 0
    except Badge.DoesNotExist:
        return 0

#
def update_data_dict(data,user,course):
    for item in data["stacks"]:
        if item["course_title"] == course.title:
            item["badges"] = all_badge_progresses(user, course)


    return data

# check progress for all badges
def all_badge_progresses(user, course):
    progresses = {}
    for b in badges:
        progresses[b[0]] = {"progress": badge_progress(b, user, course), "maximum": b[1]}

    return progresses
