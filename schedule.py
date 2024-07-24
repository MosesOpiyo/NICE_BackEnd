from django.core.management.base import BaseCommand
from django_q.models import Schedule

class Command(BaseCommand):
    help = 'Schedule the periodic task'

    def handle(self, *args, **kwargs):
        Schedule.objects.create(
            func='orders.tasks.cart_periodic_task',  # Path to your task function
            minutes=60,  # Run every minute
            repeats=-1  # Keep repeating indefinitely
        )
        self.stdout.write(self.style.SUCCESS('Successfully scheduled task'))