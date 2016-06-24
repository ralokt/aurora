from django.db.models import Q

from django.core.management.base import BaseCommand

from PlagCheck.models import Suspicion, SuspicionState
from PlagCheck.verification import plagcheck_verify


class Command(BaseCommand):
    help = 'Triggers a plagiarism check for documents which haven\'t checked yet'

    def handle(self, *args, **options):
        suspicions = list(Suspicion.objects.filter(Q(state=SuspicionState.SUSPECTED.value) | Q(state=SuspicionState.SUSPECTED_SELF_PLAGIARISM.value)))

        for suspicion in suspicions:
            plagcheck_verify(suspicion.suspect_doc)
