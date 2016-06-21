from sys import stdout
from datetime import datetime

from django.core.management.base import BaseCommand

from PlagCheck.verification import plagcheck_store_and_verify

class Command(BaseCommand):
    help = 'Triggers a plagiarism check for documents which haven\'t checked yet'

    def handle(self, *args, **options):

        with open(args[0], 'r') as f:
            content = f.read()

        plagcheck_store_and_verify(
            elaboration_id=0,
            text=content,
            user_id=0,
            user_name='filter',
            submission_time=datetime.now(),
            is_filter=True,
        )
