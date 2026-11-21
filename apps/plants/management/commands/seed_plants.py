
import hashlib
import random
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from PIL import Image, ImageDraw, ImageFont

from apps.plants.models import Plant


# ==========================================
# PLANT DATA - 120 PLANTS
# ==========================================

PLANT_DATA = {
    "TREE": [
        "Oak", "Pine", "Maple", "Birch", "Willow",
        "Cedar", "Cypress", "Redwood", "Eucalyptus",
        "Palm Tree", "Olive Tree", "Acacia",
        "Baobab", "Banyan", "Elm", "Ash Tree",
        "Beech", "Fir Tree", "Jacaranda",
        "Magnolia Tree",
    ],

    "FRUIT": [
        "Apple", "Banana", "Orange", "Mango",
        "Strawberry", "Watermelon", "Pineapple",
        "Grape", "Peach", "Pear", "Cherry",
        "Blueberry", "Raspberry", "Kiwi",
        "Papaya", "Pomegranate", "Guava",
        "Fig", "Lemon", "Dragon Fruit",
    ],

    "VEGETABLE": [
        "Carrot", "Potato", "Tomato", "Cucumber",
        "Broccoli", "Cauliflower", "Spinach",
        "Lettuce", "Cabbage", "Eggplant",
        "Bell Pepper", "Onion", "Garlic",
        "Radish", "Beetroot", "Zucchini",
        "Pumpkin", "Celery", "Asparagus",
        "Green Beans",
    ],

    "FLOWER": [
        "Rose", "Tulip", "Sunflower", "Daisy",
        "Orchid", "Lily", "Lavender Flower",
        "Jasmine", "Hibiscus", "Marigold",
        "Daffodil", "Carnation", "Peony",
        "Lotus", "Iris", "Chrysanthemum",
        "Poppy", "Hydrangea", "Dahlia",
        "Gardenia",
    ],

    "HERB": [
        "Basil", "Mint", "Rosemary", "Thyme",
        "Oregano", "Parsley", "Cilantro",
        "Dill", "Sage", "Chives",
        "Lemongrass", "Bay Laurel", "Tarragon",
        "Marjoram", "Spearmint", "Peppermint",
        "Lemon Balm", "Fennel", "Chamomile",
        "Culinary Lavender",
    ],

    "SUCCULENT": [
        "Aloe Vera", "Echeveria", "Jade Plant",
        "Zebra Haworthia", "Snake Plant",
        "Burro's Tail", "String of Pearls",
        "Panda Plant", "Ponytail Palm",
        "Christmas Cactus", "Prickly Pear Cactus",
        "Barrel Cactus", "Moon Cactus",
        "Golden Sedum", "Lithops",
        "Aeonium", "Agave", "Kalanchoe",
        "Hens and Chicks", "String of Hearts",
    ],
}


# ==========================================
# DESCRIPTIONS
# ==========================================

DESCRIPTIONS = {
    "TREE": (
        "{name} is a tree belonging to a diverse group "
        "of woody perennial plants. Trees contribute "
        "to natural landscapes, provide habitat for "
        "wildlife, and play an important role in "
        "terrestrial ecosystems."
    ),

    "FRUIT": (
        "{name} is a fruit commonly associated with "
        "food cultivation and agriculture. Fruit crops "
        "vary in flavor, texture, growing requirements, "
        "and seasonal availability."
    ),

    "VEGETABLE": (
        "{name} is a vegetable crop used in food "
        "preparation. Vegetable crops are cultivated "
        "in home gardens and farms, with growing "
        "conditions differing by species."
    ),

    "FLOWER": (
        "{name} is a flowering plant admired for "
        "its ornamental qualities. Flowering plants "
        "vary widely in their shape, color, fragrance, "
        "and growing requirements."
    ),

    "HERB": (
        "{name} is an herb associated with culinary "
        "or aromatic applications. Herbs are grown "
        "in gardens and containers, and their "
        "growing needs vary by variety."
    ),

    "SUCCULENT": (
        "{name} belongs to a group of plants known "
        "for their distinctive appearance and, in "
        "many cases, water-storing tissues. "
        "Succulents are popular in plant collections "
        "and ornamental gardening."
    ),
}


USES = {
    "TREE": (
        "Landscaping, ecological planting, shade "
        "where appropriate, and supporting biodiversity."
    ),

    "FRUIT": (
        "Food preparation, fresh produce, beverages, "
        "desserts, and agricultural cultivation."
    ),

    "VEGETABLE": (
        "Cooking, fresh produce, home gardening, "
        "and agricultural production."
    ),

    "FLOWER": (
        "Ornamental gardening, floral arrangements "
        "where suitable, and landscape decoration."
    ),

    "HERB": (
        "Culinary seasoning, aromatic gardening, "
        "and home herb cultivation."
    ),

    "SUCCULENT": (
        "Indoor or outdoor ornamental displays, "
        "container gardening, and plant collections."
    ),
}


# Whether the listed plant is primarily
# being categorized as an edible crop.
EDIBLE_CATEGORIES = {
    "FRUIT",
    "VEGETABLE",
    "HERB",
}


# ==========================================
# IMAGE GENERATOR
# ==========================================

PALETTES = {
    "TREE": ((231, 241, 229), (55, 111, 70)),
    "FRUIT": ((253, 238, 222), (208, 112, 58)),
    "VEGETABLE": ((234, 243, 221), (91, 145, 64)),
    "FLOWER": ((251, 234, 240), (196, 91, 132)),
    "HERB": ((229, 243, 233), (51, 131, 91)),
    "SUCCULENT": ((224, 241, 238), (64, 139, 135)),
}


def generate_plant_image(name, category):
    seed = int(
        hashlib.sha256(name.encode("utf-8")).hexdigest()[:12],
        16,
    )
    rng = random.Random(seed)

    width, height = 900, 650
    background, accent = PALETTES[category]

    image = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(image)

    # Soft decorative background shapes
    for _ in range(18):
        x = rng.randint(-100, width)
        y = rng.randint(-100, height)
        radius = rng.randint(30, 125)

        color = tuple(
            min(255, channel + rng.randint(0, 18))
            for channel in background
        )

        draw.ellipse(
            (x, y, x + radius, y + radius),
            fill=color,
        )

    # Ground
    draw.ellipse(
        (220, 555, 680, 605),
        fill=(195, 209, 190),
    )

    # Pot
    draw.polygon(
        [(320, 440), (580, 440), (545, 575), (355, 575)],
        fill=(191, 132, 95),
    )
    draw.rounded_rectangle(
        (307, 425, 593, 452),
        radius=12,
        fill=(159, 99, 71),
    )

    # Stems
    for index in range(7):
        x_end = 450 + (index - 3) * rng.randint(32, 55)
        y_end = rng.randint(150, 320)

        draw.line(
            (450, 432, x_end, y_end),
            fill=(69, 111, 65),
            width=8,
        )

        # Leaves / petals
        for side in (-1, 1):
            cx = x_end + side * rng.randint(15, 65)
            cy = y_end + rng.randint(-25, 35)

            leaf_width = rng.randint(45, 85)
            leaf_height = rng.randint(75, 130)

            color = tuple(
                max(0, min(255, c + rng.randint(-18, 22)))
                for c in accent
            )

            draw.ellipse(
                (
                    cx - leaf_width // 2,
                    cy - leaf_height // 2,
                    cx + leaf_width // 2,
                    cy + leaf_height // 2,
                ),
                fill=color,
            )

    # Plant title
    try:
        font = ImageFont.truetype("arial.ttf", 38)
        small_font = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    draw.text(
        (35, 35),
        name,
        fill=(35, 55, 39),
        font=font,
    )

    draw.text(
        (36, 85),
        category.title(),
        fill=accent,
        font=small_font,
    )

    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=88)

    return ContentFile(buffer.getvalue())


# ==========================================
# DJANGO MANAGEMENT COMMAND
# ==========================================

class Command(BaseCommand):
    help = "Populate Planteer with 120 sample plants."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=120,
            help="Maximum number of plants to process.",
        )

        parser.add_argument(
            "--no-images",
            action="store_true",
            help="Skip image generation.",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        with_images = not options["no_images"]

        if limit < 1:
            self.stderr.write(
                self.style.ERROR("--limit must be at least 1.")
            )
            return

        User = get_user_model()

        owner = User.objects.filter(
            is_superuser=True
        ).order_by("pk").first()

        created = 0
        existing = 0
        images_created = 0
        processed = 0

        for category, names in PLANT_DATA.items():
            for name in names:

                if processed >= limit:
                    break

                processed += 1

                # Don't create duplicates on repeated runs
                plant = Plant.objects.filter(
                    name__iexact=name
                ).first()

                if plant is None:
                    plant = Plant.objects.create(
                        name=name,
                        about=DESCRIPTIONS[category].format(
                            name=name
                        ),
                        used_for=USES[category],
                        category=category,
                        is_edible=(
                            category in EDIBLE_CATEGORIES
                        ),
                        created_by=owner,
                        image="",
                    )
                    created += 1
                else:
                    existing += 1

                # Only generate a cover when missing
                if with_images and not plant.image:
                    filename = (
                        f"seed-{slugify(name)}.jpg"
                    )

                    plant.image.save(
                        filename,
                        generate_plant_image(
                            name,
                            category,
                        ),
                        save=False,
                    )
                    plant.managed_cover_path = plant.image.name
                    plant.save(update_fields=["image", "managed_cover_path"])
                    images_created += 1

            if processed >= limit:
                break

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "PLANTEER SEED COMPLETED!"
            )
        )

        self.stdout.write(
            f"Plants created: {created}"
        )
        self.stdout.write(
            f"Existing plants skipped: {existing}"
        )
        self.stdout.write(
            f"Images generated: {images_created}"
        )
        self.stdout.write(
            f"Total plants in database: "
            f"{Plant.objects.count()}"
        )
