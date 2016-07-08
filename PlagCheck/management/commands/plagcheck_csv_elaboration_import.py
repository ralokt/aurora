from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from django.core.exceptions import ValidationError
from Challenge.models import Challenge
from PlagCheck.verification import *
from sys import stdout
from django.db import connections
from PlagCheck.util.settings import PlagCheckSettings


"""
SQL queries

2014 Data
----------
COPY (SELECT elab.id, elab.user_id, challenge.title, usr.matriculation_number, elab.creation_time, elab.submission_time, elab.elaboration_text FROM "Elaboration_elaboration" elab, "Challenge_challenge" challenge, "PortfolioUser_portfoliouser" usr, "Course_course" course WHERE elab.user_id = usr.user_ptr_id AND elab.challenge_id = challenge.id) TO '/tmp/aurora_2014.pgsql.bin' BINARY;

2015/2016 Data
----------
COPY (SELECT elab.id, elab.user_id, challenge.title, usr.matriculation_number, elab.creation_time, elab.submission_time, elab.elaboration_text FROM "Elaboration_elaboration" elab, "Challenge_challenge" challenge, "AuroraUser_aurorauser" usr, "Course_course" course WHERE elab.user_id = usr.user_ptr_id AND elab.challenge_id = challenge.id) TO '/tmp/aurora_2015.pgsql.bin' BINARY;

"""

aurora_2014_export_query = """
    COPY (
      SELECT
        elab.id,
        elab.user_id,
        challenge.title,
        usr.matriculation_number,
        elab.creation_time,
        elab.submission_time,
        elab.elaboration_text
      FROM
        "Elaboration_elaboration" elab,
        "Challenge_challenge" challenge,
        "PortfolioUser_portfoliouser" usr
      WHERE
        elab.user_id = usr.user_ptr_id
      AND elab.challenge_id = challenge.id
      ) TO '/tmp/aurora_2014.csv' BINARY;
    """

class Command(BaseCommand):
    help = 'Populates database with demo data'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)

    def handle(self, *args, **options):
        #force_csv_import(options['csv'])
        import_from_binary(args[0])


def readlines(f):
    line = []
    while True:
        s = f.read(1)
        if len(s) == 0:
            if len(line) > 0:
                yield line
                line = []
            return
        if s == b'\n':
            if len(line) > 0:
                yield line
                line = []
        elif s == b'\r':
        #if s == b'\r':
            t = f.read(1)
            if t == b'\n':
                if len(line) > 0:
                    yield line
                line = []
            else:
                line.append(t)
        else:
            line.append(s)

def import_from_binary(binary_file, dry_run=False):
    import_query = """
            DROP TABLE IF EXISTS imported_tmp;
            CREATE TEMPORARY TABLE imported_2014 (
              id INT,
              user_id INT,
              title TEXT,
              matriculation_number TEXT,
              creation_time TIMESTAMP,
              submission_time TIMESTAMP,
              elaboration_text TEXT
            );
            COPY imported_2014 (
              id,
              user_id,
              title,
              matriculation_number,
              creation_time,
              submission_time,
              elaboration_text
            ) FROM %s BINARY;
            SELECT
              id,
              user_id,
              title,
              matriculation_number,
              creation_time,
              submission_time,
              elaboration_text
            FROM imported_2014;
            """
    cursor = connections[PlagCheckSettings.database].cursor()

    cursor.execute(import_query, [binary_file])

    count_valid=0
    count_invalid=0
    for row in cursor.fetchall():
        try:
            doc = plagcheck_store(
                dry_run=dry_run,
                elaboration_id=row[0],
                user_id=row[1],
                challenge=row[2],
                user_name=row[3],
                submission_time=row[5],
                text=row[6],
            )
        except ValidationError:
            doc = None

        if doc:
            count_valid += 1
        else:
            count_invalid += 1

        #percent = (100.0 / count_total) * (count_valid + count_invalid)
        percent = 0

        stdout.write("\r{0:6.2f}% {1:10} valid, {2:10} invalid or already added".format(percent, count_valid, count_invalid))
        stdout.flush()

    stdout.write("\n")

    print("Checking all unverified documents ...")
    if not dry_run:
        plagcheck_check_unverified()


def import_from_csv(csv_file, dry_run=False):
    print("Reading elaborations from csv file")
    elabs = read_elaborations_from_csv(csv_file)

    count_total = len(elabs)

    print("Adding {0} elaborations to plagcheck document store.".format(count_total))

    count_valid=0
    count_invalid=0
    for elab in elabs:
        done = False

        while not done:
            try:
                doc = plagcheck_store(
                    dry_run=dry_run,

                    text=elab['text'],
                    elaboration_id=elab['id'],
                    user_id=0,
                    user_name=elab['user'],
                    submission_time=elab['submission_time'],
                    challenge=elab['challenge']
                )
                done = True

            except OperationalError:
                pass
            except ValidationError as e:
                doc = None
                done = True

        if doc:
            count_valid += 1
        else:
            count_invalid += 1

        percent = (100.0 / count_total) * (count_valid + count_invalid)

        stdout.write("\r{0:6.2f}% {1:10} valid, {2:10} invalid or already added".format(percent, count_valid, count_invalid))
        stdout.flush()

    stdout.write("\n")

    print("Checking all unverified documents ...")
    if not dry_run:
        plagcheck_check_unverified()


def read_elaborations_from_csv(csv_file, begin_at=0):
    i = 0

    elaborations = []
    with open(csv_file, "rb") as f:
        for bytelist in readlines(f):
            #print(bytelist)
            line = b''.join(bytelist).decode("utf-8")

            if i <= begin_at:
                i += 1
                continue

            i += 1
            data = line.split(',', 5)
            try:
                elab = dict()
                elab['id'] = int(data[0])
                elab['challenge'] = data[1]
                elab['user'] = data[2]
                elab['created'] = data[3]
                elab['submission_time'] = data[4]
                elab['text'] = data[5]

            except (IndexError, ValueError) as e:
                print(data)
                raise ValueError("Error on line(%i): %s" % (i, line), e)

            elaborations.append(elab)

    return elaborations
