from django.db.models import signals

from PortfolioUser.models import PortfolioUser
from Course.models import *
from Challenge.models import Challenge


user_map = {'s0': 's0'}

def init_data(app, sender, **kwargs):
    if 'django.contrib.auth.models' == app.__name__:
        for i in range(len(list(user_map.keys()))):
            print('adding student %s of %s' % (i, len(list(user_map.keys()))))
            username = list(user_map.keys())[i]
            user = PortfolioUser(username=username)
            user.email = '%s@student.tuwien.ac.at.' % username
            user.first_name = 'Firstname_%s' % username
            user.last_name = 'Lastname_%s' % username
            user.nickname = 'Nickname_%s' % username
            user.is_staff = False
            user.is_superuser = False
            password = user_map[username]
            user.set_password(password)
            user.save()

        # create an admin user with password amanaman
        print('adding superuser')
        superuser = PortfolioUser(username='amanaman')
        superuser.set_password('amanaman')
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()


        # create courses "GSI" and "HCI"
        print('adding course gsi')
        gsi = Course(
            title='Gesellschaftliche Spannungsfelder der Informatik',
            short_title='gsi',
            description='GSI Description',
            course_number='123.456',
        )
        gsi.save()

        print('adding course hci')
        hci = Course(
            title='Human Computer Interaction',
            short_title='hci',
            description='HCI Description',
            course_number='123.457',
        )
        hci.save()


        # create course-user relations
        print('adding course-user relations')
        CourseUserRelation(course=gsi, user=user).save()
        CourseUserRelation(course=hci, user=user).save()
        CourseUserRelation(course=gsi, user=superuser).save()
        CourseUserRelation(course=gsi, user=superuser).save()


        # create challenges
        print('adding challenges')
        challenge_1 = Challenge(id=1,
            title='meine meinung',
            subtitle='meine meinung',
            description='posten sie ihre meinung zu irgendwas in drei sätzen. dabei müssen sie lediglich darauf achten, dass die drei sätze alle mit demselben buchstaben beginnen.',
            cardImageUrl='1.png',
            backgroundImageUrl='1b.png',
        ).save()

        challenge_2 = Challenge(id=2,
            title='rage-comic',
            subtitle='rage-comic',
            prerequisite=challenge_1,
            description='finden sie einen rage-comic, den sie lustig finden, und beschreiben sie kurz, warum sie ihn lustig finden. laden sie dazu den rage-comic als bild hoch, und beschreiben sie in einem satz mit genau 5 worten, warum dieser rage-comic zum schreien komisch ist.',
            cardImageUrl='2.png',
            backgroundImageUrl='2b.png',
        ).save()

        challenge_3 = Challenge(id=3,
            title='wikipedia',
            subtitle='wikipedia',
            prerequisite=challenge_2,
            description='kopieren sie 4 absätze aus einem langweiligen wikipedia-artikel und geben sie sie ab. selbst schreiben ist verboten - das würde als plagiat gewertet!',
            cardImageUrl='3.png',
            backgroundImageUrl='3b.png',
        ).save()

        challenge_4 = Challenge(id=4,
            title='wissenschaft',
            subtitle='wissenschaft',
            prerequisite=challenge_3,
            description='finden sie einen pseudowissenschaftlichen artikel und laden sie ihn hier hoch.',
            cardImageUrl='4.png',
            backgroundImageUrl='4b.png',
        ).save()

        challenge_5 = Challenge(id=5,
            title='ping',
            subtitle='ping',
            description='laden sie ein bild im png-format hoch. das bild muss allerdings genau quadratisch sein. schreiben sie nichts dazu (geht ja auch nicht).',
            cardImageUrl='5.png',
            backgroundImageUrl='5b.png',
        ).save()

        challenge_6 = Challenge(id=6,
            title='advice animal',
            subtitle='advice animal',
            prerequisite=challenge_5,
            description='finden sie ein »advice animal« bild, das hier überhaupt nicht dazupasst. laden sie das bild hoch, und posten sie einen text dazu, der stattdessen auf dem bild stehen sollte. der muss auch gar nicht witzig sein.',
            cardImageUrl='6.png',
            backgroundImageUrl='6b.png',
        ).save()

        challenge_7 = Challenge(id=7,
            title='animated gif',
            subtitle='animated gif',
            prerequisite=challenge_6,
            description='suchen sie ein lustiges animated gif und posten sie es. schreiben sie als text 10 x das wort "lustig" dazu.',
            cardImageUrl='7.png',
            backgroundImageUrl='7b.png',
        ).save()

        challenge_8 = Challenge(id=8,
            title='das bin ich',
            subtitle='das bin ich',
            prerequisite=challenge_7,
            description='posten sie drei bilder von sich, und beschreiben sie kurz, wer auf den fotos zu sehen ist. die bilder von sich brauchen auch gar nicht wirklich von ihnen zu sein, sondern einfach nur von irgendwem, der ihnen ähnlich schaut. oder auch nicht.',
            cardImageUrl='8.png',
            backgroundImageUrl='8b.png',
        ).save()

        challenge_9 = Challenge(id=9,
            title='sherlock',
            subtitle='sherlock',
            description='finden sie einen ausschnitt der britischen fernsehserie »sherlock« auf youtube und posten sie ihn hier. schreiben sie ausserdem dazu, dass sie sherlock saucool finden (in eigenen worten!)',
            cardImageUrl='9.png',
            backgroundImageUrl='9b.png',
        ).save()

        challenge_10 = Challenge(id=10,
            title='schmetterling',
            subtitle='schmetterling',
            prerequisite=challenge_9,
            description='laden sie zwei bilder von schmetterlingen hoch, und schreiben sie eine kleine geschichte (max. 10 worte), in denen die schmetterlinge vorkommen.',
            cardImageUrl='4.png',
            backgroundImageUrl='4b.png',
        ).save()

        # create course-challenge relations
        print('adding course-challenge relations')
        CourseChallengeRelation(course=gsi, challenge_id=1).save()
        CourseChallengeRelation(course=gsi, challenge_id=2).save()
        CourseChallengeRelation(course=gsi, challenge_id=3).save()
        CourseChallengeRelation(course=gsi, challenge_id=4).save()
        CourseChallengeRelation(course=gsi, challenge_id=5).save()
        CourseChallengeRelation(course=gsi, challenge_id=6).save()
        CourseChallengeRelation(course=gsi, challenge_id=7).save()
        CourseChallengeRelation(course=gsi, challenge_id=8).save()
        CourseChallengeRelation(course=gsi, challenge_id=9).save()
        CourseChallengeRelation(course=gsi, challenge_id=10).save()

        CourseChallengeRelation(course=hci, challenge_id=4).save()
        CourseChallengeRelation(course=hci, challenge_id=6).save()
        CourseChallengeRelation(course=hci, challenge_id=7).save()
        CourseChallengeRelation(course=hci, challenge_id=8).save()


signals.post_syncdb.connect(init_data)