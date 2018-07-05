from django.core.management.base import BaseCommand

from mbou.models import StaffMember


class Command(BaseCommand):
    def handle(self, *args, **options):
        staff = StaffMember.objects.all()
        staff.delete()
