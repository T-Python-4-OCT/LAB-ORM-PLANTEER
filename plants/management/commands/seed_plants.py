import json
from pathlib import Path

from django.contrib.staticfiles import finders
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from plants.models import Plant


class Command(BaseCommand):
    help = "Add the bundled plants using their static photographs."

    def handle(self, *args, **options):
        folder = Path(__file__).resolve().parents[2] / "seed_data"
        entries = json.loads((folder / "plants.json").read_text(encoding="utf-8"))
        missing = [entry["slug"] for entry in entries
                   if not finders.find(f'img/{entry["slug"]}.webp')]
        if missing:
            raise CommandError("Missing bundled photographs: " + ", ".join(missing))

        created = 0
        with transaction.atomic():
            for entry in entries:
                filename = f'{entry["slug"]}.webp'
                static_image = f"img/{filename}"
                if Plant.objects.filter(static_image=static_image).exists() or Plant.objects.filter(name=entry["name"]).exists():
                    continue
                fields = {key: value for key, value in entry.items() if key != "slug"}
                Plant.objects.create(static_image=static_image, **fields)
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Added {created} plants."))
