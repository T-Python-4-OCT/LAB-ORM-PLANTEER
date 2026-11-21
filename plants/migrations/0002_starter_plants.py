from django.db import migrations


def add_starter_plants(apps, schema_editor):
    Plant = apps.get_model("plants", "Plant")
    plants = Plant.objects.using(schema_editor.connection.alias)
    examples = [
        {
            "name": "Snake plant",
            "category": "houseplant",
            "is_edible": False,
            "about": "Dracaena trifasciata has stiff, upright leaves with bands of green.",
            "used_for": "Grown indoors as an ornamental foliage plant.",
            "image": "samples/snake-plant.webp",
        },
        {
            "name": "Moth orchid",
            "category": "flower",
            "is_edible": False,
            "about": "Phalaenopsis orchids bear open, rounded flowers along arching stems.",
            "used_for": "Grown as an ornamental flowering houseplant.",
            "image": "samples/orchid.webp",
        },
        {
            "name": "Rosemary",
            "category": "herb",
            "is_edible": True,
            "about": "Salvia rosmarinus is an evergreen shrub with narrow, fragrant leaves.",
            "used_for": "The leaves season roasted vegetables, bread and other savory dishes.",
            "image": "samples/rosemary.webp",
        },
        {
            "name": "Calendula",
            "category": "flower",
            "is_edible": True,
            "about": (
                "Calendula officinalis, also called pot marigold, has bright orange or yellow, "
                "daisy-like flower heads."
            ),
            "used_for": "Grown for garden color. Culinary-grade petals are used as a garnish.",
            "image": "samples/calendula.webp",
        },
        {
            "name": "Cinnamon basil",
            "category": "herb",
            "is_edible": True,
            "about": (
                "This variety of Ocimum basilicum is named for the warm, cinnamon-like scent of "
                "its leaves."
            ),
            "used_for": "The fragrant leaves flavor teas, fruit dishes and savory recipes.",
            "image": "samples/basil.webp",
        },
    ]
    for example in examples:
        image = example["image"]
        if not plants.filter(image=image).exists():
            plants.create(**example)


class Migration(migrations.Migration):
    dependencies = [("plants", "0001_initial")]
    operations = [migrations.RunPython(add_starter_plants, migrations.RunPython.noop)]
