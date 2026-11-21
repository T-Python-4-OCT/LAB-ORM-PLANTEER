from django.core.management.base import BaseCommand
from plants.models import Plant

PLANTS = [
    {"name": "Date Palm", "scientific_name": "Phoenix dactylifera", "about": "An iconic desert palm cultivated for generations. Its sweet dates are a traditional food across the Arabian Peninsula, and the tree offers valuable shade in arid places.", "native_to": "Middle East and North Africa", "used_for": "Dates, shade, and traditional crafts.", "category": "tree", "is_edible": True, "image": "plants/date-palm.jpg"},
    {"name": "Olive", "scientific_name": "Olea europaea", "about": "A long-lived evergreen tree with silvery leaves and small fruits. Olives have shaped food and landscapes across the Mediterranean for thousands of years.", "native_to": "Mediterranean Basin", "used_for": "Olive oil, table olives, and shade.", "category": "tree", "is_edible": True, "image": "plants/olive.jpg"},
    {"name": "Lemon", "scientific_name": "Citrus limon", "about": "A fragrant citrus tree with bright, tart fruit. In warm climates it can flower and fruit through much of the year.", "native_to": "Northeast India and nearby regions", "used_for": "Cooking, drinks, and preserves.", "category": "fruit", "is_edible": True, "image": "plants/lemon.jpg"},
    {"name": "Tomato", "scientific_name": "Solanum lycopersicum", "about": "A sun-loving garden plant grown for juicy fruits. Hundreds of varieties range from tiny sweet cherries to large heirloom tomatoes.", "native_to": "Western South America", "used_for": "Salads, sauces, roasting, and fresh eating.", "category": "vegetable", "is_edible": True, "image": "plants/tomato.jpg"},
]

class Command(BaseCommand):
    help = "Add the starter plants to the database."

    def handle(self, *args, **options):
        for data in PLANTS:
            Plant.objects.update_or_create(name=data["name"], defaults=data)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(PLANTS)} starter plants."))
