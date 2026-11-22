# Planteer

A Django and SQLite botanical catalog for the [LAB-ORM-PLANTEER assignment](https://github.com/M3TZ305/LAB-ORM-PLANTEER). Browse plants by category and edibility, search by name or use, maintain catalog entries, and leave comments. The contact form saves messages to a public messages page.

## Run locally

Use Python 3.12 or later. From the project folder in PowerShell, run:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_plants
.\.venv\Scripts\python.exe manage.py runserver
```

Open [Planteer on localhost](http://127.0.0.1:8000/). Reuse the existing `.venv` if one is already configured. The seed command can be rerun and uses the photographs bundled in the repository.

Visit `/contact/messages/` to read submitted messages.

## Project structure

- `main` contains the home page, contact form, and public messages page.
- `plants` contains the catalog, combined filters, ORM search, plant CRUD, and visitor comments.
- `templates` and `static` contain the shared layout, page templates, styles, and theme preference. Django serves uploaded images from `media` in local development.
- `plants/seed_data` contains the sample records. Their photographs live in `static/img`. User uploads go to `media/img` (plant photos), `media/pdf` (PDF attachments), or `media/fiels` (other supported attachments).
- The original assignment includes the [main wireframes](https://github.com/M3TZ305/LAB-ORM-PLANTEER/blob/12dbb734dc5daa62f73eb721b0dc057b03d24031/assets/main-wireframe.png), [contact wireframes](https://github.com/M3TZ305/LAB-ORM-PLANTEER/blob/12dbb734dc5daa62f73eb721b0dc057b03d24031/assets/contact-wireframe.png), and [UML](https://github.com/M3TZ305/LAB-ORM-PLANTEER/blob/12dbb734dc5daa62f73eb721b0dc057b03d24031/assets/uml.png).

The local settings enable Django's development server. For a provisioned environment, set `DJANGO_DEBUG=0`, `DJANGO_SECRET_KEY`, and `DJANGO_ALLOWED_HOSTS`, and configure your server to serve collected static files and uploaded media.

## Verification

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test
```
