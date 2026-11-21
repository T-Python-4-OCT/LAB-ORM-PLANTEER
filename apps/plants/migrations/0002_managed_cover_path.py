import csv
from pathlib import Path

from django.conf import settings
from django.db import migrations, models
from django.utils.text import slugify


def identify_managed_covers(apps, schema_editor):
    from apps.plants.management.commands.seed_plants import PALETTES, generate_plant_image

    plant_model = apps.get_model("plants", "Plant")
    plants = plant_model.objects.using(schema_editor.connection.alias)
    credits_path = Path(settings.BASE_DIR) / "photo_review" / "credits.csv"
    credited_covers = set()
    if credits_path.is_file():
        with credits_path.open(encoding="utf-8-sig", newline="") as handle:
            credited_covers = {
                (row["plant_id"], row["image_file"])
                for row in csv.DictReader(handle)
                if row.get("role") == "cover" and row.get("source")
            }

    for plant in plants.exclude(image="").iterator():
        path = plant.image.name
        verified = (str(plant.pk), path) in credited_covers
        seed_path = f"plants/covers/seed-{slugify(plant.name)}.jpg"
        if not verified and path == seed_path and plant.category in PALETTES:
            expected = generate_plant_image(plant.name, plant.category).read()
            try:
                with plant.image.open("rb") as image:
                    verified = image.read(len(expected) + 1) == expected
            except OSError:
                pass
        if verified:
            plants.filter(pk=plant.pk, image=path).update(managed_cover_path=path)


class Migration(migrations.Migration):
    dependencies = [("plants", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="plant",
            name="managed_cover_path",
            field=models.CharField(blank=True, editable=False, max_length=100),
        ),
        migrations.RunPython(identify_managed_covers, migrations.RunPython.noop),
    ]
