# LAB-ORM-PLANTEER

## Run Planteer

A complete Django application with a responsive botanical design, SQLite persistence, plant CRUD, combined search/category/edibility filters, related plants, comments, and a public contact-message board. The implementation uses two apps: `main` and `plants`, and shared Django template inheritance.

On Windows, run `./start.ps1`, then visit **http://127.0.0.1:8000/**. The script uses the existing virtual environment or creates one with an installed Python 3.11+.

Manual setup:

```powershell
py -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe manage.py migrate
.venv/Scripts/python.exe manage.py seed_plants
.venv/Scripts/python.exe manage.py runserver
```

Run checks with `.venv/Scripts/python.exe manage.py test` and `.venv/Scripts/python.exe manage.py check`. `seed_plants` is repeatable and preserves existing records. Uploaded images are saved in `media/plants/`; starter photographs are served locally from `static/images/`. Restore starter images with `.venv/Scripts/python.exe scripts/download_images.py` if needed. Photography is sourced from Unsplash; original photo IDs are retained in filenames and the seed command. Fonts are DM Sans and Manrope from Google Fonts, with system fallbacks.

This is a local educational app: plant editing is open to visitors, as requested. Contact names/messages are public with an explicit notice before submission; emails are visible only through Django admin. To use admin, run `manage.py createsuperuser`. Before internet deployment, add authentication/authorization for editing and moderation, use a private production secret, set `DJANGO_DEBUG=0`, configure allowed hosts and production media/static serving, and replace the development server with a production server.

---

Replacement photos: [Snake plant by cottonbro studio](https://www.pexels.com/photo/potted-dracaena-trifasciata-plant-on-vintage-couch-4575430/) and [white moth orchid](https://www.pexels.com/photo/beautiful-orchid-in-close-up-view-20013414/), from Pexels. The download script keeps these replacements local under the original asset keys.

Matched collection photos: [Monstera](https://www.pexels.com/photo/a-green-leaves-on-a-pot-6954409/), [golden pothos](https://www.pexels.com/photo/golden-pothos-in-black-pot-11838530/), and [Echeveria](https://www.pexels.com/photo/close-up-of-succulents-in-a-pot-16753186/). These photos are downloaded locally; `seed_plants` also corrects the original starter image URLs without overwriting custom uploads or other image URLs.


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
