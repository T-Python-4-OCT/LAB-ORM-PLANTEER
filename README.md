# Planteer

LAB-ORM-PLANTEER: a plant database for plants lovers, built with Django and SQLite, following the task's wireframe and UML.

## Run it

```
python -m venv venv
venv\Scripts\activate            # Windows   (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_plants     # adds the 6 sample plants (photos are inside the project)
python manage.py runserver
```

## Pages

| Page | Path |
|---|---|
| Home | `/` |
| All Plants (filter by `category` and `is_edible`) | `plants/all/` |
| Plant Detail (related plants + comments) | `plants/<plant_id>/detail/` |
| Add Plant | `plants/new/` |
| Update Plant | `plants/<plant_id>/update/` |
| Delete Plant | `plants/<plant_id>/delete/` |
| Search | `plants/search/` |
| Contact Us (bonus) | `contact/` |
| Messages from Users (bonus) | `contact/messages/` |

## Apps

- `main`: home, contact us, messages from users (`Contact` model).
- `plants`: plants and comments (`Plant` and `Comment` models).

## Models

- `Plant`: name, about, used_for, image, category (TextChoices), is_edible, created_at
- `Comment`: plant (ForeignKey to Plant, `related_name="comments"`), full_name, content, created_at
- `Contact`: first_name, last_name, email, message, created_at

Forms are ModelForms (`plants/forms.py`, `main/forms.py`). Related plants use `filter(category=...)` with `exclude(id=...)`.

## Images

- Fixed images: `main/static/main/images/hero.jpg` (home header) and `contact.jpg` (contact page).
- Sample plant photos: `plants/seed_images/`. `seed_plants` copies them to `media/images/`.
- `python manage.py seed_plants --reset` deletes all the plants, then adds the 6 samples again.
- All photos are free photos from [Pexels](https://www.pexels.com).
