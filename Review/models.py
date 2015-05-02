from django.contrib.contenttypes.models import ContentType
from django.db import models

from Comments.models import Comment


class Review(models.Model):
    elaboration = models.ForeignKey('Elaboration.Elaboration')
    creation_time = models.DateTimeField(auto_now_add=True)
    submission_time = models.DateTimeField(null=True)
    reviewer = models.ForeignKey('AuroraUser.AuroraUser')

    NOTHING = 'N'
    FAIL = 'F'
    SUCCESS = 'S'
    AWESOME = 'A'
    APPRAISAL_CHOICES = (
        (NOTHING, 'Not even trying'),
        (FAIL, 'Fail'),
        (SUCCESS, 'Success'),
        (AWESOME, 'Awesome'),
    )
    appraisal = models.CharField(max_length=1, choices=APPRAISAL_CHOICES, null=True)

    def __unicode__(self):
        return str(self.id)

    def get_elaboration_author(self):
        return self.elaboration.user

    @staticmethod
    def get_open_review(challenge, user):
        open_reviews = Review.objects.filter(elaboration__challenge=challenge, submission_time__isnull=True,
                                             reviewer=user)
        if open_reviews:
            return open_reviews[0]
        else:
            return None

    @staticmethod
    def get_review_amount(elaboration):
        # TODO: evaluate if unsubmitted reviews should be excluded from the count
        # .exclude(submission_time__isnull=True))
        return len(Review.objects.filter(elaboration=elaboration))

    def get_comments(self):
        return Comment.objects.filter(content_type=ContentType.objects.get_for_model(Review), object_id=self.id)

    @staticmethod
    def query_reviews_with_questions():
        content_type = ContentType.objects.get_for_model(Review)
        # Review.objects.annotate()


class ReviewConfig(models.Model):
    # in hours
    candidate_offset_min = models.IntegerField(default=0)
    candidate_offset_max = models.IntegerField(default=0)

    @staticmethod
    def get_candidate_offset_min():
        config = ReviewConfig.objects.all()
        if config.count() == 0:
            return 0
        else:
            return config[0].candidate_offset_min

    @staticmethod
    def get_candidate_offset_max():
        config = ReviewConfig.objects.all()
        if config.count() == 0:
            return 0
        else:
            return config[0].candidate_offset_max