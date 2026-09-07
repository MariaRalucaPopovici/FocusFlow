from django.core.management.base import BaseCommand
from wellbeing.models import DopamineMenuItem

ITEMS = [
    ("starters", "Quick walk"),
    ("starters", "Stretching"),
    ("starters", "Change your location"),
    ("starters", "Gratitude journal"),
    ("mains", "Exercise"),
    ("mains", "Cooking or baking"),
    ("mains", "Reading"),
    ("mains", "Meeting a friend"),
    ("sides", "Listen to a podcast or playlist"),
    ("sides", "Colouring or drawing"),
    ("sides", "Knitting or crocheting"),
    ("desserts", "Scroll social media"),
    ("desserts", "Binge-watch a show"),
    ("desserts", "A special treat or snack"),
    ("specials", "Concert or gig"),
    ("specials", "Buy something nice for yourself"),
    ("specials", "Day trip somewhere new"),
    ("salads", "Workout"),
    ("salads", "Meal prepping"),
]

class Command(BaseCommand):
    help = "Seeds the Dopamine Menu with starter items across all six categories."

    def handle(self, *args, **options):
        created = 0
        for category, title in ITEMS:
            obj, was_created = DopamineMenuItem.objects.update_or_create(
                title=title,
                defaults={"category": category, "active": True},
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Processed {len(ITEMS)} dopamine menu items ({created} newly created)."))