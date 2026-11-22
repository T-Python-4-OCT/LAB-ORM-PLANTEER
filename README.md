# 🌿 Planteer — Plant Database For Plants Lovers

A Django website to discover, add, filter, search and comment on plants.

## Pages

| Page | Path | App |
|---|---|---|
| Home | `/` | main |
| All Plants (filter by `category` and `is_edible`) | `plants/all/` | plants |
| Plant Detail (+ related plants + comments) | `plants/<plant_id>/detail/` | plants |
| Add new plant | `plants/new/` | plants |
| Update plant | `plants/<plant_id>/update/` | plants |
| Delete plant (confirmation page, deletes on POST) | `plants/<plant_id>/delete/` | plants |
| Search (name, about, used for) | `plants/search/?q=...` | plants |
| Add a comment (POST) | `plants/<plant_id>/comments/add/` | plants |
| (Bonus) Contact Us | `contact/` | main |
| (Bonus) Contact Us Messages | `contact/messages/` | main |

## Models — all in `plants/models.py`, one class per table

```
Plant                          Comment                        Contact
-----                          -------                        -------
id (PK)                        id (PK)                        id (PK)
name        CharField          plant  ForeignKey -> Plant     first_name  CharField
about       TextField          full_name  CharField           last_name   CharField
used_for    TextField          content    TextField           email       EmailField
image       ImageField         created_at DateTimeField       message     TextField
category    CharField (TextChoices)                           created_at  DateTimeField
is_edible   BooleanField
created_at  DateTimeField (auto_now_add)
```

**Plant 1 ──< many Comment**: every comment stores `plant_id`, a foreign key pointing to the
primary key of one plant (`on_delete=CASCADE`, `related_name="comments"` → `plant.comments.all()`).

Related plants on the detail page use a filter:
`Plant.objects.filter(category=plant.category).exclude(pk=plant.pk)[:3]`

## Project structure

```
Planteer/
├── manage.py
├── Planteer/            settings, root urls (main at "/", plants at "plants/")
├── main/                home, contact, contact messages + the shared layout
│   ├── templates/main/  base.html (template inheritance), home, contact, contact_messages, partials/
│   └── static/main/     css/style.css, js/main.js, img/favicon.svg
├── plants/              Plant, Comment, Contact models · CRUD · filter · search · comments
│   ├── templates/plants/ all_plants, plant_detail, plant_form (add + update), plant_delete, search
│   ├── management/commands/seed_plants.py
│   └── seed_images/     the 20 real plant photos used by seed_plants
└── media/plants/default.jpg   placeholder photo
```

## Run it

```bash
python -m venv venv
venv\Scripts\activate            # Windows   (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
cd Planteer
python manage.py migrate
python manage.py seed_plants     # adds 20 real plants with their real photos
python manage.py runserver
```

`seed_plants` copies each plant's photo from `plants/seed_images/` (no internet needed).
Running it twice never duplicates plants. The included `db.sqlite3` already has the 20 plants with their photos.

Tests: `python manage.py test` (26 tests).

Plant photos: Wikimedia Commons contributors, under their Creative Commons licenses — the file name of
each photo is listed in `plants/management/commands/seed_plants.py`; its Commons page shows the author and license.
