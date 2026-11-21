"""Add the 6 sample plants with their photos:  python manage.py seed_plants

The photos are inside the project (plants/seed_images/), so no internet is needed.
Plants that already exist (same name) are skipped, so it is safe to run more than once.
Add --reset to delete all the plants first:  python manage.py seed_plants --reset
"""

from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from plants.models import Plant

IMAGES = Path(__file__).resolve().parents[2] / "seed_images"

# Added in this order, so the newest three (shown first on the home page) are Pear, Watermelon and Beetroot
PLANTS = [
    {
        "name": "Echeveria", "image": "echeveria.jpg", "category": "succulent", "is_edible": False,
        "about": "A small succulent whose thick leaves grow in the shape of a rose. It needs sun and very little water.",
        "used_for": "Grown in small pots to decorate homes, offices and balconies.",
    },
    {
        "name": "Mint", "image": "mint.jpg", "category": "herb", "is_edible": True,
        "about": "A fragrant herb with fresh-smelling green leaves. It grows fast in pots and wet places.",
        "used_for": "Added to tea and drinks, and used in salads, cooking and desserts.",
    },
    {
        "name": "Olive", "image": "olive.jpg", "category": "tree", "is_edible": True,
        "about": "An evergreen tree from the Mediterranean that can live for hundreds of years and handles drought.",
        "used_for": "Olives are eaten after curing, olive oil is pressed from them, and the wood is used for carving.",
    },
    {
        "name": "Beetroot", "image": "beetroot.jpg", "category": "vegetables", "is_edible": True,
        "about": "A root vegetable with a deep red color and a sweet taste. Its leaves can be eaten too.",
        "used_for": "Used in salads, juices and soups, and as a natural red food color.",
    },
    {
        "name": "Watermelon", "image": "watermelon.jpg", "category": "fruit", "is_edible": True,
        "about": "A trailing plant with big fruits: green outside, red, sweet and full of water inside.",
        "used_for": "Eaten fresh in summer, and used in juices and fruit salads.",
    },
    {
        "name": "Pear", "image": "pear.jpg", "category": "fruit", "is_edible": True,
        "about": "A fruit tree with sweet, juicy fruits that are wide at the bottom and narrow at the top.",
        "used_for": "Eaten fresh, baked in desserts, and made into juice and jam.",
    },
]


class Command(BaseCommand):
    help = "Add the 6 sample plants with their photos"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete all the plants before adding")

    def handle(self, *args, **options):
        if options["reset"]:
            for plant in Plant.objects.all():
                plant.image.delete(save=False)
            Plant.objects.all().delete()
            self.stdout.write("All plants deleted.")

        added = 0
        for item in PLANTS:
            if Plant.objects.filter(name=item["name"]).exists():
                self.stdout.write(f"- {item['name']}: already added, skipped")
                continue
            plant = Plant(
                name=item["name"], about=item["about"], used_for=item["used_for"],
                category=item["category"], is_edible=item["is_edible"],
            )
            with open(IMAGES / item["image"], "rb") as photo:
                plant.image.save(item["image"], File(photo), save=False)   # copied to media/images/
            plant.save()
            added += 1
            self.stdout.write(self.style.SUCCESS(f"+ {item['name']}"))

        self.stdout.write(self.style.SUCCESS(f"Done: {added} plants added."))
