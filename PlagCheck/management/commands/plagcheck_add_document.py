from sys import stdout
from datetime import datetime
from optparse import make_option
from pprint import pprint

from django.core.management.base import BaseCommand
from django.forms import model_to_dict

from PlagCheck.verification import plagcheck_store, plagcheck_verify
from PlagCheck.models import Result, Suspicion

class Command(BaseCommand):
    help = 'Triggers a plagiarism check for documents which haven\'t checked yet'

    option_list = BaseCommand.option_list + (
        make_option('--filter',
            action='store_true',
            dest='filter',
            default=False,
            help='Use document as a filter'),
        )

    def handle(self, *args, **options):

        with open(args[0], 'r') as f:
            content = f.read()

        doc = plagcheck_store(
            always_create=True,

            elaboration_id=0,
            text=content,
            user_id=0,
            user_name='document',
            submission_time=datetime.now(),
            is_filter=options['filter'],
        )

        result_dict = plagcheck_verify(doc).wait()

        out = {}

        result = Result.objects.get(pk=result_dict['id'])

        suspicions = Suspicion.objects.filter(result=result)

        out['result'] = model_to_dict(result)

        out['suspicions'] = []
        for suspicion in suspicions:
            suspicion_dict = model_to_dict(suspicion)

            suspicion_dict['similar_doc'] = model_to_dict(suspicion.similar_doc)

            out['suspicions'].append(suspicion_dict)

        pprint(out)
