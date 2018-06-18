from django.core.management.base import BaseCommand, CommandError
import datetime

from mbou.models import LessonTiming


class Command(BaseCommand):
    help = "creates fake timetables."

    def handle(self, *args, **options):
        number = 9
        START_TIME_HOUR = 8
        START_TIME_MINUTES = 0
        LESSON_DURATION = 45
        SMALL_PAUSE = 10
        BIG_PAUSE = 15
        DEFAULT = 0
        hour = START_TIME_HOUR
        minute = START_TIME_MINUTES
        for i in range(1, number):
            les = LessonTiming()
            les.number = i
            if i != 1:
                minute += SMALL_PAUSE
            if minute > 59:
                hour += 1
                minute = minute % 60
            les.start = datetime.time(hour=hour, minute=minute, second=DEFAULT, microsecond=DEFAULT)
            minute += LESSON_DURATION
            if minute > 59:
                hour += 1
                minute = minute % 60
            les.end = datetime.time(hour=hour, minute=minute, second=DEFAULT, microsecond=DEFAULT)
            les.save()
            self.stdout.write("[%d] added lessontiming %d" % (i, i))
