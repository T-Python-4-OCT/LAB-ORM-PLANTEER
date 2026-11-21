from django.db import migrations


def expand_starter_catalog(apps, schema_editor):
    Plant = apps.get_model("plants", "Plant")
    plants = Plant.objects.using(schema_editor.connection.alias)
    examples = [
        {
            "name": "Golden chain tree",
            "category": "tree",
            "is_edible": False,
            "about": (
                "Laburnum anagyroides is a small deciduous tree with hanging clusters of yellow "
                "flowers."
            ),
            "used_for": "Grown as an ornamental tree for its spring flowers.",
            "image": "samples/golden-chain.webp",
        },
        {
            "name": "Sweet orange",
            "category": "fruit",
            "is_edible": True,
            "about": "Citrus × sinensis is an evergreen citrus tree with round, sweet fruit.",
            "used_for": "The fruit is eaten fresh or juiced, and the zest flavors baked goods and sauces.",
            "image": "samples/orange.webp",
        },
        {
            "name": "Romaine lettuce",
            "category": "vegetable",
            "is_edible": True,
            "about": (
                "This type of Lactuca sativa forms an upright head of crisp leaves with sturdy "
                "central ribs."
            ),
            "used_for": "The leaves add crunch to salads, sandwiches and wraps.",
            "image": "samples/romaine.webp",
        },
        {
            "name": "Golden pothos",
            "category": "houseplant",
            "is_edible": False,
            "about": (
                "Epipremnum aureum is a climbing vine with heart-shaped leaves often streaked "
                "with yellow."
            ),
            "used_for": "Grown indoors in hanging baskets or trained up a support.",
            "image": "samples/pothos.webp",
        },
        {
            "name": "Garden strawberry",
            "category": "fruit",
            "is_edible": True,
            "about": (
                "Fragaria × ananassa is a low-growing plant that spreads by runners and bears red "
                "fruit."
            ),
            "used_for": "The fruit is eaten fresh or made into jams and desserts.",
            "image": "samples/strawberry.webp",
        },
        {
            "name": "Broccoli",
            "category": "vegetable",
            "is_edible": True,
            "about": (
                "This form of Brassica oleracea grows a dense head of green flower buds on a "
                "thick stem."
            ),
            "used_for": "The florets and tender stem can be steamed, roasted or stir-fried.",
            "image": "samples/broccoli.webp",
        },
        {
            "name": "English lavender",
            "category": "flower",
            "is_edible": True,
            "about": (
                "Lavandula angustifolia has slender gray-green leaves and fragrant purple flower "
                "spikes."
            ),
            "used_for": (
                "Grown for its scent and flowers. Culinary-grade buds are used to flavor baked "
                "goods."
            ),
            "image": "samples/lavender.webp",
        },
        {
            "name": "Pomegranate",
            "category": "fruit",
            "is_edible": True,
            "about": (
                "Punica granatum is a shrub or small tree whose leathery fruit holds clusters of "
                "juicy arils."
            ),
            "used_for": "The arils are eaten fresh or used in salads and juices.",
            "image": "samples/pomegranate.webp",
        },
        {
            "name": "Carrot",
            "category": "vegetable",
            "is_edible": True,
            "about": (
                "Cultivated Daucus carota has feathery leaves and a taproot that can be orange, "
                "purple, yellow or white."
            ),
            "used_for": "The root is eaten raw or used in soups, stews and roasted dishes.",
            "image": "samples/carrot.webp",
        },
    ]
    for example in examples:
        if not plants.filter(image=example["image"]).exists():
            plants.create(**example)


class Migration(migrations.Migration):
    dependencies = [("plants", "0002_starter_plants")]
    operations = [migrations.RunPython(expand_starter_catalog, migrations.RunPython.noop)]
