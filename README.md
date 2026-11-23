# LAB-ORM-PLANTEER – Planteer 🌿

**Planteer** is a plant database for plant lovers, built with Django.
Visitors can browse real plants, filter and search them, add, edit and delete plants, and comment on each plant.

## Features

- **Two apps:** `main` (home, contact) and `plants` (plants, comments, search).
- **Plant CRUD** with a `ModelForm`, image upload and a delete confirmation page.
- **All Plants page** with filters by `category` and `is_edible` (GET parameters, kept after submit) and pagination.
- **Search page** by name and description using `Q` objects and `icontains`.
- **Comments:** visitors add comments on the plant detail page (no login), newest first.
- **Related plants** from the same category, excluding the current plant.
- **Browse by category** on the home page with plant counts (`annotate` + `Count`).
- **Contact Us** form and **Messages** page (bonus).
- Template inheritance (`base.html` + partials), responsive design and a custom 404 page.
- 54 automated tests.

## Pages

| Page | URL |
|---|---|
| Home | `/` |
| All Plants | `/plants/all/` |
| Plant Detail | `/plants/<plant_id>/detail/` |
| Add Plant | `/plants/new/` |
| Update Plant | `/plants/<plant_id>/update/` |
| Delete Plant | `/plants/<plant_id>/delete/` |
| Search | `/plants/search/` |
| Contact Us | `/contact/` |
| Contact Messages | `/contact/messages/` |

## Run the project (Git Bash)

```bash
git clone https://github.com/muathhhh/LAB-ORM-PLANTEER.git
cd LAB-ORM-PLANTEER
py -m venv venv
source venv/Scripts/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata plants
python manage.py runserver
```

Then open http://127.0.0.1:8000/

Run the tests:

```bash
python manage.py test
```

## Tech

Django 6.1 · Python 3.15 · SQLite · Pillow · HTML/CSS (no CSS framework)

---

# Assignment

## Using what you learned, Create a new website called "Planteer" , this website has the following pages/paths:
- Home page `/`
- All Plants page : `plants/all/`
- Plant Detail Page : `plants/<plant_id>/detail/`
- Add new plant page : `plants/new/`
- Update plant page : `plants/<plant_id>/update/`,
- Delete Plant : `plants/<plant_id>/delete/`
- Search Page : `plants/search/`
- (Bonus) Contact Us page : `contact/`
- (Bonus) Contact Us Messages page : `contact/messages/`


### Notes:
- Use templates & template inheritance.
- The website must be responsive (looks good on big and small screens)
- In all plants page, user can filter by `category` and `is_edible`.
- For the images, backgrounds, fonts you can use whatever you like. As for the content like categories,  make sure you add real plants with real plants images.
- Use at least 2 apps, one main and one for the plants.
- Add a related `Comment` model on the plants (fields: plant relation, full_name, content, created_at).  So, visitors can add comments on the plants.
- In Plant detail page , Add related plants (based on the same category, use filter !)
  
## wireframe for the main pages
<img width="1771" style="width:100%" alt="Screenshot 2024-03-19 at 2 27 18 PM" src="assets/main-wireframe.png">

## Contact pages wireframe:
<img width="1015" style="width:100%" alt="Screenshot 2024-03-19 at 3 22 17 PM" src="assets/contact-wireframe.png">


## UML for the model `Plant` &  `Contact` Model 
<img width="618" style="width:100%; height:auto;" alt="Screenshot 2024-03-19 at 3 16 01 PM" src="assets/uml.png">
