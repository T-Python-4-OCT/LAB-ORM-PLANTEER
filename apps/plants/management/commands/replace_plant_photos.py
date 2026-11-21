
import csv
import json
import time
from hashlib import sha256
from html import escape, unescape
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import uuid4

import requests
from PIL import Image

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, transaction
from django.db.models import F
from django.utils.html import strip_tags
from django.utils.text import slugify

from apps.plants.models import PhotoImportProgress, Plant, PlantImage


API_URL = "https://commons.wikimedia.org/w/api.php"

DATA_DIR = Path(settings.BASE_DIR) / "photo_review"
MANIFEST = DATA_DIR / "candidates.json"
PREVIEW = DATA_DIR / "review.html"
SELECTIONS = DATA_DIR / "selections.csv"
CREDITS = DATA_DIR / "credits.csv"

# Replace with your actual project contact.
USER_AGENT = (
    "PlanteerEducation/1.0 "
    "(contact: aaq_224@hotmail.com)"
)

SEARCH_TERMS = {
    "Oak": "Quercus oak",
    "Pine": "Pinus pine",
    "Maple": "Acer maple",
    "Birch": "Betula birch",
    "Willow": "Salix willow",
    "Rose": "Rosa flower",
    "Aloe Vera": "Aloe vera",
    "Sunflower": "Helianthus annuus",
    "Basil": "Ocimum basilicum",
    "Tulip": "Tulipa flower",
    "Lavender Flower": "Lavandula flower",
}

BLOCKED_WORDS = (
    "drawing",
    "illustration",
    "painting",
    "diagram",
    "logo",
    "herbarium",
    "clipart",
    "map",
)


def clean(value):
    return unescape(strip_tags(value or "")).strip()


def metadata_value(metadata, key):
    return clean(metadata.get(key, {}).get("value", ""))


def allowed_license(value):
    name = value.lower().replace("-", " ").strip()

    return (
        name.startswith("cc by")
        or name.startswith("cc0")
        or name.startswith("public domain")
        or name.startswith("pd ")
    )


def is_managed_cover(plant):
    return bool(plant.image and plant.image.name == plant.managed_cover_path)


class Command(BaseCommand):
    help = "Review and import multiple Wikimedia plant photos."

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            choices=["preview", "apply"],
        )

        parser.add_argument(
            "--limit",
            type=int,
            help="Maximum plants to attempt (preview defaults to 5)",
        )

        parser.add_argument(
            "--all",
            action="store_true",
        )

    def handle(self, *args, **options):
        if "your-email@example.com" in USER_AGENT:
            self.stderr.write(
                self.style.ERROR(
                    "Set your real contact in USER_AGENT first."
                )
            )
            return

        DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        if options["action"] == "preview":
            if options["limit"] is None:
                options["limit"] = 5
            self.create_preview(options)
        else:
            if options["limit"] is not None and options["limit"] < 1:
                raise CommandError("--limit must be positive.")
            if options["all"] and options["limit"] is not None:
                raise CommandError("Use either --all or --limit.")
            self.apply_selections(options["limit"])

    def get_session(self):
        session = requests.Session()

        session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        })

        return session

    # =====================================
    # WIKIMEDIA SEARCH
    # =====================================

    def find_candidates(self, session, plant):
        term = SEARCH_TERMS.get(
            plant.name,
            f"{plant.name} plant",
        )

        queries = [
            term,
            f"{plant.name} leaves",
        ]

        results = []
        seen = set()

        for query in queries:
            params = {
                "action": "query",
                "format": "json",
                "formatversion": "2",
                "generator": "search",
                "gsrsearch": query,
                "gsrnamespace": 6,
                "gsrlimit": 20,
                "prop": "imageinfo",
                "iiprop": "url|size|extmetadata",
                "iiurlwidth": 650,
            }

            response = session.get(
                API_URL,
                params=params,
                timeout=30,
            )
            response.raise_for_status()

            pages = response.json().get(
                "query", {}
            ).get("pages", [])

            for page in pages:
                title = page.get("title", "")
                lower_title = title.lower()

                if title in seen:
                    continue

                if not lower_title.endswith(
                    (".jpg", ".jpeg")
                ):
                    continue

                if any(
                    word in lower_title
                    for word in BLOCKED_WORDS
                ):
                    continue

                infos = page.get("imageinfo", [])

                if not infos:
                    continue

                info = infos[0]

                if (
                    info.get("width", 0) < 450
                    or info.get("height", 0) < 300
                ):
                    continue

                metadata = info.get(
                    "extmetadata", {}
                )

                license_name = metadata_value(
                    metadata,
                    "LicenseShortName",
                )

                if not allowed_license(license_name):
                    continue

                thumb = (
                    info.get("thumburl")
                    or info.get("url")
                )

                original = info.get("url")

                if not thumb or not original:
                    continue

                results.append({
                    "title": title,
                    "thumb": thumb,
                    "url": original,
                    "source": info.get(
                        "descriptionurl", ""
                    ),
                    "author": metadata_value(
                        metadata, "Artist"
                    ),
                    "license": license_name,
                    "license_url": metadata_value(
                        metadata, "LicenseUrl"
                    ),
                })

                seen.add(title)

                if len(results) >= 4:
                    return results

            time.sleep(0.5)

        return results

    # =====================================
    # PREVIEW
    # =====================================

    def create_preview(self, options):
        if options["limit"] < 1:
            self.stderr.write(
                "--limit must be positive."
            )
            return

        plants = [
            plant
            for plant in Plant.objects.order_by("id")
            if is_managed_cover(plant)
        ]

        if not options["all"]:
            plants = plants[:options["limit"]]

        session = self.get_session()
        manifest = []

        for plant in plants:
            try:
                candidates = self.find_candidates(
                    session,
                    plant,
                )

                manifest.append({
                    "id": plant.pk,
                    "name": plant.name,
                    "candidates": candidates,
                })

                self.stdout.write(
                    f"{plant.name}: "
                    f"{len(candidates)} candidates"
                )

            except (
                requests.RequestException,
                ValueError,
            ) as error:
                self.stderr.write(
                    f"FAILED {plant.name}: {error}"
                )

            time.sleep(1)

        MANIFEST.write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        self.create_html(manifest)

        self.stdout.write(
            self.style.SUCCESS(
                f"Review page created: {PREVIEW}"
            )
        )

    # =====================================
    # HTML REVIEW PAGE
    # =====================================

    def create_html(self, manifest):
        sections = []

        for plant in manifest:
            cards = []

            for index, photo in enumerate(
                plant["candidates"]
            ):
                cards.append(f"""
                <article class="photo-card">

                    <img
                        src="{escape(photo['thumb'], quote=True)}"
                        alt="{escape(photo['title'], quote=True)}"
                        loading="lazy">

                    <div class="photo-content">

                        <strong>
                            {escape(photo['title'])}
                        </strong>

                        <small>
                            {escape(photo['license'])}
                        </small>

                        <a
                            href="{escape(photo['source'], quote=True)}"
                            target="_blank"
                            rel="noopener noreferrer">
                            View Source
                        </a>

                        <label class="cover-option">
                            <input
                                type="radio"
                                name="cover-{plant['id']}"
                                value="{index}">
                            Main Cover
                        </label>

                        <label class="gallery-option">
                            <input
                                type="checkbox"
                                name="gallery-{plant['id']}"
                                value="{index}">
                            Add to Gallery
                        </label>

                    </div>
                </article>
                """)

            if not cards:
                cards.append(
                    '<p class="empty">No photos found.</p>'
                )

            sections.append(f"""
            <section class="plant-section"
                     data-plant-id="{plant['id']}">

                <div class="plant-heading">
                    <div>
                        <h2>{escape(plant['name'])}</h2>
                        <p>Plant ID: {plant['id']}</p>
                    </div>
                    <span class="selection-count">
                        0 gallery photos
                    </span>
                </div>

                <div class="photo-grid">
                    {''.join(cards)}
                </div>

            </section>
            """)

        html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1">

<title>Planteer Photo Review</title>

<style>
:root {
    --primary: #315a40;
    --background: #f4f7f4;
    --border: #dfe7df;
    --text: #1c2c20;
    --muted: #718075;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: var(--background);
    color: var(--text);
    font-family: Arial, sans-serif;
}

header {
    position: sticky;
    top: 0;
    z-index: 10;
    background: white;
    border-bottom: 1px solid var(--border);
    padding: 20px 4%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    flex-wrap: wrap;
}

header h1 {
    margin: 0 0 7px;
    font-size: 25px;
}

header p {
    margin: 0;
    color: var(--muted);
}

button {
    background: var(--primary);
    border: none;
    border-radius: 6px;
    color: white;
    padding: 13px 22px;
    font-weight: 700;
    cursor: pointer;
}

main {
    width: min(1550px, 94%);
    margin: 35px auto;
}

.plant-section {
    background: white;
    padding: 24px;
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: 28px;
}

.plant-heading {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
}

.plant-heading h2 {
    margin: 0 0 5px;
}

.plant-heading p {
    margin: 0;
    color: var(--muted);
}

.selection-count {
    color: var(--primary);
    font-size: 13px;
    font-weight: 600;
}

.photo-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 15px;
}

.photo-card {
    min-width: 0;
    border: 1px solid var(--border);
    border-radius: 9px;
    overflow: hidden;
}

.photo-card > img {
    width: 100%;
    height: 190px;
    object-fit: cover;
    display: block;
}

.photo-content {
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.photo-content strong {
    font-size: 12px;
    overflow-wrap: anywhere;
}

.photo-content small {
    color: var(--muted);
}

.photo-content a {
    color: var(--primary);
    font-size: 13px;
}

.cover-option,
.gallery-option {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 11px;
    cursor: pointer;
    border-radius: 5px;
    font-size: 13px;
    font-weight: 600;
}

.cover-option {
    background: #edf3ed;
}

.gallery-option {
    background: #f6f7fa;
}

input {
    accent-color: var(--primary);
}

.empty {
    color: var(--muted);
}

@media (max-width: 950px) {
    .photo-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 550px) {
    .photo-grid {
        grid-template-columns: 1fr;
    }
}
</style>

</head>

<body>

<header>
    <div>
        <h1>Planteer Photo Review</h1>
        <p>
            Choose one Cover and up to 3 Gallery images.
        </p>
    </div>

    <button onclick="exportSelections()">
        Export Selections CSV
    </button>
</header>

<main>
""" + "\n".join(sections) + """
</main>

<script>
document.querySelectorAll(
    ".plant-section"
).forEach(section => {

    const covers = section.querySelectorAll(
        'input[type="radio"]'
    );

    const galleries = section.querySelectorAll(
        'input[type="checkbox"]'
    );

    function updateCount() {
        const selected = [...galleries].filter(
            input => input.checked
        );

        section.querySelector(
            ".selection-count"
        ).textContent =
            selected.length + " gallery photos";
    }

    covers.forEach(cover => {
        cover.addEventListener("change", () => {
            galleries.forEach(gallery => {
                if (gallery.value === cover.value) {
                    gallery.checked = false;
                }
            });

            updateCount();
        });
    });

    galleries.forEach(gallery => {
        gallery.addEventListener("change", () => {

            const selectedCover = section.querySelector(
                'input[type="radio"]:checked'
            );

            if (
                selectedCover &&
                selectedCover.value === gallery.value &&
                gallery.checked
            ) {
                gallery.checked = false;

                alert(
                    "The cover image cannot also be in the gallery."
                );
            }

            const selected = [...galleries].filter(
                input => input.checked
            );

            if (selected.length > 3) {
                gallery.checked = false;

                alert(
                    "Maximum 3 gallery images per plant."
                );
            }

            updateCount();
        });
    });
});


function exportSelections() {
    const rows = [
        ["plant_id", "cover_index", "gallery_indices"]
    ];

    document.querySelectorAll(
        ".plant-section"
    ).forEach(section => {

        const plantId = section.dataset.plantId;

        const cover = section.querySelector(
            'input[type="radio"]:checked'
        );

        const galleries = [
            ...section.querySelectorAll(
                'input[type="checkbox"]:checked'
            )
        ].map(input => input.value);

        if (!cover && galleries.length === 0) {
            return;
        }

        if (!cover) {
            alert(
                "Select a main Cover for plant ID " + plantId
            );
            throw new Error("Missing cover");
        }

        rows.push([
            plantId,
            cover.value,
            galleries.join("|")
        ]);
    });

    if (rows.length === 1) {
        alert("Please select at least one plant.");
        return;
    }

    const content = rows.map(
        row => row.join(",")
    ).join("\\r\\n");

    const blob = new Blob(
        [content],
        {type: "text/csv;charset=utf-8"}
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "selections.csv";
    link.click();

    setTimeout(
        () => URL.revokeObjectURL(url),
        1000
    );
}
</script>

</body>
</html>
"""

        PREVIEW.write_text(
            html,
            encoding="utf-8",
        )

    # =====================================
    # IMAGE DOWNLOAD
    # =====================================

    def download_image(self, session, url):
        response = session.get(
            url,
            timeout=45,
            stream=True,
        )
        response.raise_for_status()

        content = bytearray()

        for chunk in response.iter_content(
            chunk_size=65536
        ):
            content.extend(chunk)

            if len(content) > 15_000_000:
                raise ValueError(
                    "Image exceeds 15 MB."
                )

        image = Image.open(BytesIO(content))
        image.load()

        if image.width < 450 or image.height < 300:
            raise ValueError(
                "Image resolution too low."
            )

        image = image.convert("RGB")
        image.thumbnail((1400, 1100))

        output = BytesIO()

        image.save(
            output,
            format="JPEG",
            quality=85,
            optimize=True,
        )

        return output.getvalue()

    # =====================================
    # IMAGE CREDITS
    # =====================================

    def load_credits(self):
        credits = []

        if not CREDITS.exists():
            return credits

        with CREDITS.open(
            encoding="utf-8-sig",
            newline="",
        ) as file:
            credits = list(csv.DictReader(file))

        return credits

    def save_credits(self, credits):
        fields = list(dict.fromkeys([
            "plant_id", "plant", "role", "image_file", "author",
            "license", "license_url", "source",
            *(field for credit in credits for field in credit),
        ]))
        with NamedTemporaryFile(
            dir=CREDITS.parent, encoding="utf-8-sig", newline="", mode="w", delete=False
        ) as file:
            temporary_path = Path(file.name)
            try:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                writer.writerows(credits)
            except BaseException:
                file.close()
                temporary_path.unlink(missing_ok=True)
                raise
        try:
            temporary_path.replace(CREDITS)
        finally:
            temporary_path.unlink(missing_ok=True)

    def sync_credits(self):
        # SQLite acquires the write lock before reading the ledger or CSV.
        with transaction.atomic():
            progress = PhotoImportProgress.objects.filter(completed=True)
            progress.update(completed=F("completed"))
            credits = self.load_credits()
            known = {
                (credit["plant_id"], credit["role"], credit["image_file"], credit["source"])
                for credit in credits
            }
            additions = []
            for entries in progress.order_by("pk").values_list("credits", flat=True):
                for credit in entries:
                    key = (credit["plant_id"], credit["role"], credit["image_file"], credit["source"])
                    if key not in known:
                        additions.append(credit)
                        known.add(key)
            if additions:
                credits.extend(additions)
                self.save_credits(credits)
            return credits

    def selected_photos(self, row, candidates):
        cover_index = int(row["cover_index"])
        gallery_text = row.get("gallery_indices", "").strip()
        galleries = [int(value) for value in gallery_text.split("|")] if gallery_text else []
        indices = [cover_index, *galleries]
        if (
            len(galleries) > 3
            or len(indices) != len(set(indices))
            or any(not 0 <= index < len(candidates) for index in indices)
        ):
            raise ValueError("Select one cover and up to three distinct gallery indices.")
        return [candidates[index] for index in indices]

    def pending_selections(self, manifest, rows):
        latest = {}
        attempts = {}
        for progress in PhotoImportProgress.objects.order_by("-attempted_at", "-pk"):
            attempts[progress.plant_id, progress.fingerprint] = progress.attempted_at
            if progress.completed:
                latest.setdefault(progress.plant_id, progress.fingerprint)

        plants = Plant.objects.in_bulk(int(row["plant_id"]) for row in rows)
        pending = []
        seen = set()
        protected = 0
        for row in rows:
            plant_id = int(row["plant_id"])
            if plant_id in seen:
                continue
            seen.add(plant_id)
            plant = plants.get(plant_id)
            if plant is None:
                raise ValueError(f"Plant {plant_id} does not exist.")
            if not is_managed_cover(plant):
                protected += 1
                continue
            photos = self.selected_photos(row, manifest[plant_id])
            fingerprint = sha256(json.dumps(photos, sort_keys=True).encode("utf-8")).hexdigest()
            if latest.get(plant_id) != fingerprint:
                pending.append((plant, photos, fingerprint))
        # Attempt untouched selections first, then the least recently attempted.
        pending.sort(key=lambda entry: (
            (entry[0].pk, entry[2]) in attempts,
            attempts.get((entry[0].pk, entry[2])),
        ))
        return pending, protected

    def import_plant(self, session, plant, photos, fingerprint, credits):
        if not is_managed_cover(plant):
            raise ValueError("Cover is protected.")
        plant_id = str(plant.pk)
        previous_cover = plant.image.name
        gallery = list(plant.images.values_list("pk", "image", "position"))
        gallery_files = {image for _, image, _ in gallery}
        positions = [position for _, _, position in gallery]
        credited = {
            (credit["role"], credit["source"], credit["image_file"])
            for credit in credits if credit["plant_id"] == plant_id
        }
        cover, *gallery_photos = photos
        new_photos = []
        if ("cover", cover["source"], previous_cover) not in credited:
            new_photos.append(("cover", cover))
        gallery_sources = {
            source for role, source, image in credited
            if role == "gallery" and image in gallery_files
        }
        slots = max(0, 3 - len(gallery))
        for photo in gallery_photos:
            if slots and photo["source"] not in gallery_sources:
                new_photos.append(("gallery", photo))
                gallery_sources.add(photo["source"])
                slots -= 1

        # Decode every new selection before touching media, credits, or plant data.
        downloads = [
            (role, photo, self.download_image(session, photo.get("download_url") or photo["url"]))
            for role, photo in new_photos
        ]
        new_credits = []
        saved_files = []
        position = max(positions, default=0)
        try:
            with transaction.atomic():
                # Recheck provenance and serialize updates before writing media.
                locked = Plant.objects.filter(
                    pk=plant.pk, image=previous_cover, managed_cover_path=previous_cover,
                ).exclude(image="").update(managed_cover_path=F("managed_cover_path"))
                if not locked or gallery != list(plant.images.values_list("pk", "image", "position")):
                    raise ValueError("Cover or gallery changed during download. Retry the selection.")
                latest = PhotoImportProgress.objects.filter(
                    plant=plant, completed=True
                ).order_by("-attempted_at", "-pk").first()
                if latest and latest.fingerprint == fingerprint:
                    return []
                for role, photo, data in downloads:
                    filename = f"commons-{role}-{plant.pk}-{uuid4().hex}.jpg"
                    if role == "cover":
                        image = plant.image
                    else:
                        position += 1
                        gallery_image = PlantImage(
                            plant=plant,
                            position=position,
                            alt_text=f"{plant.name} - {photo['title'].removeprefix('File:')}"[:200],
                        )
                        image = gallery_image.image
                    image.save(filename, ContentFile(data), save=False)
                    saved_files.append((image.storage, image.name))
                    if role == "cover":
                        Plant.objects.filter(pk=plant.pk).update(
                            image=image.name, managed_cover_path=image.name
                        )
                    else:
                        gallery_image.save()
                    new_credits.append({
                        "plant_id": plant_id,
                        "plant": plant.name,
                        "role": role,
                        "image_file": image.name,
                        "author": photo["author"],
                        "license": photo["license"],
                        "license_url": photo["license_url"],
                        "source": photo["source"],
                    })

                progress, _ = PhotoImportProgress.objects.get_or_create(
                    plant=plant, fingerprint=fingerprint,
                )
                progress.credits = [*progress.credits, *new_credits]
                progress.completed = True
                progress.save()
        except Exception:
            for storage, name in reversed(saved_files):
                try:
                    storage.delete(name)
                except OSError as error:
                    self.stderr.write(f"Failed to remove new file {name}: {error}")
            raise
        return new_credits

    def apply_selections(self, limit=None):
        if not MANIFEST.exists() or not SELECTIONS.exists():
            raise CommandError("Missing candidate manifest or selections CSV. Run preview first.")

        try:
            manifest = {
                item["id"]: item["candidates"]
                for item in json.loads(MANIFEST.read_text(encoding="utf-8"))
            }
            with SELECTIONS.open(encoding="utf-8-sig", newline="") as file:
                pending, protected = self.pending_selections(manifest, list(csv.DictReader(file)))
            credits = self.sync_credits()
        except (KeyError, ValueError, OSError, DatabaseError) as error:
            raise CommandError(f"Could not prepare photo import: {error}") from error

        batch = pending[:limit]
        failed = 0
        with self.get_session() as session:
            for plant, photos, fingerprint in batch:
                try:
                    credits.extend(self.import_plant(session, plant, photos, fingerprint, credits))
                except (
                    KeyError, ValueError, OSError, DatabaseError, requests.RequestException,
                    Image.DecompressionBombError,
                ) as error:
                    failed += 1
                    progress, created = PhotoImportProgress.objects.get_or_create(
                        plant=plant, fingerprint=fingerprint,
                    )
                    if not created and not progress.completed:
                        progress.save(update_fields=["attempted_at"])
                    self.stderr.write(f"FAILED plant {plant.pk} ({plant.name}): {error}")
                else:
                    self.stdout.write(f"COMPLETED plant {plant.pk} ({plant.name})")
                time.sleep(1)

        try:
            self.sync_credits()
        except (OSError, DatabaseError) as error:
            raise CommandError(
                f"Could not publish credits CSV. Committed credits will be retried next run: {error}"
            ) from error
        self.stdout.write(
            f"Attempted: {len(batch)}. Completed: {len(batch) - failed}. "
            f"Pending: {len(pending) - len(batch) + failed}. Protected: {protected}."
        )
        if failed:
            raise CommandError(f"{failed} plant(s) failed and remain pending.")

