from django.core.management.base import BaseCommand
from tracker.models import Category
class Command(BaseCommand):
    help = "Create the default expense categories"
    def handle(self, *args, **kwargs):
        names = ["Food", "Transport", "Shopping", "Bills", "Health", "Education", "Entertainment", "Other"]
        for name in names:
            Category.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Default categories created."))
