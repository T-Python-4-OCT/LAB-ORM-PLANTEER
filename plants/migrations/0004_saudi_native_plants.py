from django.db import migrations, models


def add_saudi_native_plants(apps, schema_editor):
    Plant = apps.get_model("plants", "Plant")
    plants = Plant.objects.using(schema_editor.connection.alias)
    examples = [
        {
            "name": "Samr",
            "category": "tree",
            "is_edible": False,
            "about": (
                "Vachellia tortilis, or السمر, is a thorny tree native to Saudi Arabia. "
                "Mature trees often have a broad, umbrella-shaped crown."
            ),
            "used_for": "Its broad crown provides shade, and livestock browse its leaves and pods.",
            "image": "samples/samr.webp",
        },
        {
            "name": "Ghaf",
            "category": "tree",
            "is_edible": True,
            "about": (
                "Prosopis cineraria, known as الغاف, is a drought-tolerant tree native to Saudi Arabia. "
                "It has fine compound leaves and long, narrow pods."
            ),
            "used_for": (
                "It provides shade and forage. The young pods are eaten as a vegetable in parts "
                "of its native range."
            ),
            "image": "samples/ghaf.webp",
        },
        {
            "name": "Fringed lavender",
            "category": "shrub",
            "is_edible": True,
            "about": (
                "Lavandula dentata is a fragrant shrub native to Saudi Arabia, "
                "with toothed leaves and purple flower spikes."
            ),
            "used_for": (
                "Grown for its scented foliage and purple flowers. "
                "It is also used as an herbal tea."
            ),
            "image": "samples/fringed-lavender.webp",
        },
        {
            "name": "Doum palm",
            "category": "tree",
            "is_edible": True,
            "about": (
                "Hyphaene thebaica, or الدوم, is a fan palm native to Saudi Arabia. "
                "Its trunk can fork into several branches."
            ),
            "used_for": (
                "Its ripe fruit is eaten or used to make drinks, and its leaves are used in "
                "weaving."
            ),
            "image": "samples/doum.webp",
        },
        {
            "name": "Hummayd",
            "category": "vegetable",
            "is_edible": True,
            "about": (
                "Rumex vesicarius, known as الحماض, is a leafy annual native to Saudi Arabia. "
                "It has fleshy green leaves and often develops pinkish fruit clusters."
            ),
            "used_for": "Its tart leaves are traditionally eaten in Saudi Arabia.",
            "image": "samples/hummayd.webp",
        },
        {
            "name": "Arfaj",
            "category": "shrub",
            "is_edible": False,
            "about": (
                "Rhanterium epapposum, known as العرفج, is a desert shrub native to Saudi Arabia "
                "with small leaves and yellow flower heads."
            ),
            "used_for": "It is used as camel forage and planted in dry landscapes.",
            "image": "samples/arfaj.webp",
        },
        {
            "name": "Sidr",
            "category": "tree",
            "is_edible": True,
            "about": (
                "Ziziphus spina-christi, or السدر, is a thorny tree native to Saudi Arabia, "
                "with glossy leaves and small round fruit."
            ),
            "used_for": "Its ripe fruit is eaten, and its blossoms provide nectar for sidr honey.",
            "image": "samples/sidr.webp",
        },
    ]
    for example in examples:
        if not plants.filter(image=example["image"]).exists():
            plants.create(**example)


class Migration(migrations.Migration):
    dependencies = [("plants", "0003_expand_starter_catalog")]
    operations = [
        migrations.AlterField(
            model_name="plant",
            name="category",
            field=models.CharField(
                max_length=20,
                choices=[
                    ("herb", "Herb"),
                    ("flower", "Flower"),
                    ("houseplant", "Houseplant"),
                    ("tree", "Tree"),
                    ("shrub", "Shrub"),
                    ("fruit", "Fruit"),
                    ("vegetable", "Vegetable"),
                ],
            ),
        ),
        migrations.RunPython(add_saudi_native_plants, migrations.RunPython.noop),
    ]
