"""Seed the database with real plants and their photos from Wikipedia.

Usage:  python manage.py seed_plants
Running it again skips plants that already exist.
"""
import json
import re
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from plants.models import Plant

USER_AGENT = 'PlanteerSeed/1.0 (educational Django project)'

# (name, wikipedia article, category, is_edible, about, used_for)
PLANTS = [
    ('Date Palm', 'Phoenix_dactylifera', 'tree', True,
     'A flowering palm cultivated for its sweet edible fruit. Native to the Middle East and North Africa, '
     'it has been grown in the Arabian Peninsula for thousands of years.',
     'Fresh and dried dates, date syrup (dibs), baking, and the leaves are used for weaving baskets and mats.'),
    ('Olive Tree', 'Olive', 'tree', True,
     'A small evergreen tree native to the Mediterranean Basin, known for its silvery-green leaves '
     'and long life — some olive trees are over 1,000 years old.',
     'Olives are eaten cured and pressed into olive oil, used in cooking, cosmetics and soap.'),
    ('Oak', 'Oak', 'tree', False,
     'A large hardwood tree of the genus Quercus, with lobed leaves and acorns. Oaks can live for '
     'centuries and support a huge range of wildlife.',
     'Strong timber for furniture, flooring and wine barrels; shade tree in parks.'),
    ('Mango', 'Mango', 'fruit', True,
     'A juicy stone fruit from the tropical tree Mangifera indica, native to South Asia. '
     'It is one of the most widely cultivated fruits in the tropics.',
     'Eaten fresh, in juices, smoothies, chutneys, desserts and dried as snacks.'),
    ('Pomegranate', 'Pomegranate', 'fruit', True,
     'A fruit-bearing shrub whose round fruit holds hundreds of ruby-red juicy seeds (arils). '
     'It originated in the region from Iran to northern India.',
     'Fresh arils, juice, pomegranate molasses in cooking, and salads.'),
    ('Strawberry', 'Strawberry', 'fruit', True,
     'A widely grown hybrid plant of the genus Fragaria, cultivated for its bright red, '
     'sweet and aromatic fruit.',
     'Eaten fresh, in jams, desserts, milkshakes and as a flavoring.'),
    ('Tomato', 'Tomato', 'vegetable', True,
     'The edible berry of Solanum lycopersicum, native to western South America. '
     'Botanically a fruit, it is used as a vegetable in cooking.',
     'Salads, sauces, soups, ketchup and countless dishes around the world.'),
    ('Carrot', 'Carrot', 'vegetable', True,
     'A root vegetable, typically orange, rich in beta-carotene. Domesticated from wild carrot '
     'native to Europe and Southwestern Asia.',
     'Eaten raw, cooked in stews and soups, juiced, and used in cakes.'),
    ('Spinach', 'Spinach', 'vegetable', True,
     'A leafy green flowering plant native to central and western Asia, valued for its '
     'iron- and vitamin-rich leaves.',
     'Salads, cooked dishes, pastries (fatayer), smoothies and soups.'),
    ('Mint', 'Mentha', 'herb', True,
     'An aromatic perennial herb with a cool, refreshing flavor. It spreads quickly and '
     'grows well in moist soil.',
     'Mint tea, garnishes, salads like tabbouleh, desserts and herbal remedies.'),
    ('Basil', 'Basil', 'herb', True,
     'A culinary herb of the mint family, native to tropical regions from central Africa '
     'to Southeast Asia, with fragrant green leaves.',
     'Pesto, Italian and Thai cooking, salads, and herbal teas.'),
    ('Rose', 'Rose', 'flower', False,
     'A woody perennial flowering plant of the genus Rosa, with over three hundred species '
     'and thousands of cultivars, famous for its fragrant blooms.',
     'Ornamental gardens, bouquets, perfume and rose water.'),
    ('Sunflower', 'Common_sunflower', 'flower', True,
     'A tall annual plant with a large yellow flower head that follows the sun when young. '
     'Native to the Americas.',
     'Sunflower seeds as snacks, sunflower oil for cooking, and ornamental use.'),
    ('Aloe Vera', 'Aloe_vera', 'succulent', False,
     'A succulent plant with thick, fleshy leaves filled with a clear gel. It is native to '
     'the Arabian Peninsula and grows well in dry climates.',
     'Skin care, soothing sunburns and minor burns, cosmetics and as a houseplant.'),
    ('Echeveria', 'Echeveria', 'succulent', False,
     'A genus of rosette-forming succulents native to Mexico and Central America, '
     'admired for their geometric shape and pastel colors.',
     'Ornamental houseplants, rock gardens and succulent arrangements.'),

    # --- More trees ---
    ('Ghaf Tree', 'Prosopis_cineraria', 'tree', True,
     'A drought-tolerant evergreen tree native to the deserts of Arabia and South Asia. '
     'It is the national tree of the UAE and survives on very little water.',
     'Shade and shelter in the desert, animal fodder, firewood, and its young pods are cooked as a vegetable.'),
    ('Sidr Tree', 'Ziziphus_spina-christi', 'tree', True,
     'A thorny evergreen tree native to the Middle East and North Africa, known for its small '
     'sweet fruit (nabq) and the famous sidr honey made from its flowers.',
     'Fruit eaten fresh or dried, sidr honey, and leaves used as a natural hair and skin cleanser.'),
    ('Neem Tree', 'Azadirachta_indica', 'tree', False,
     'A fast-growing evergreen tree from the Indian subcontinent that thrives in hot, dry climates. '
     'Every part of it has traditional uses.',
     'Natural insect repellent, neem oil for skin and hair, twigs used as tooth-cleaning sticks, and shade.'),

    # --- More fruits ---
    ('Fig', 'Common_fig', 'fruit', True,
     'One of the first plants cultivated by humans, the fig tree grows soft, sweet fruit '
     'full of tiny seeds. Native to the Middle East and western Asia.',
     'Eaten fresh or dried, in jams, desserts and salads.'),
    ('Lemon', 'Lemon', 'fruit', True,
     'A small evergreen citrus tree whose yellow, sour fruit is rich in vitamin C. '
     'Probably originated in northeast India.',
     'Lemon juice in drinks and cooking, zest in baking, cleaning products and fragrances.'),
    ('Banana', 'Banana', 'fruit', True,
     'A large herbaceous plant that produces elongated, sweet fruit in hanging clusters. '
     'One of the most eaten fruits in the world.',
     'Eaten fresh, in smoothies, desserts, banana bread and chips.'),
    ('Grape', 'Grape', 'fruit', True,
     'A woody vine of the genus Vitis bearing clusters of small round berries, green, red or purple. '
     'Grown since ancient times in the Middle East.',
     'Fresh grapes, raisins, juice, vinegar, and grape leaves stuffed with rice (warak enab).'),
    ('Watermelon', 'Watermelon', 'fruit', True,
     'A vine-like flowering plant originally from Africa. Its large fruit has a green rind '
     'and sweet, juicy red flesh that is over 90% water.',
     'Eaten fresh on hot days, in juices, salads, and roasted seeds as a snack.'),

    # --- More vegetables ---
    ('Potato', 'Potato', 'vegetable', True,
     'A starchy tuber of the plant Solanum tuberosum, native to the Andes in South America. '
     'It is one of the world\'s most important food crops.',
     'Fries, mashed potatoes, stews, baking and chips.'),
    ('Cucumber', 'Cucumber', 'vegetable', True,
     'A creeping vine of the gourd family producing long, green, refreshing fruits. '
     'Originated in South Asia.',
     'Salads, pickles, yogurt dips, and cooling skin care.'),
    ('Eggplant', 'Eggplant', 'vegetable', True,
     'A plant of the nightshade family grown for its glossy purple fruit. '
     'Widely used in Middle Eastern and Mediterranean cooking.',
     'Baba ganoush, maqluba, moussaka, grilled and fried dishes.'),

    # --- More herbs ---
    ('Rosemary', 'Rosemary', 'herb', True,
     'A fragrant evergreen shrub with needle-like leaves, native to the Mediterranean region. '
     'It tolerates drought very well.',
     'Seasoning for meat, chicken and bread, herbal tea and essential oil.'),
    ('Thyme', 'Thyme', 'herb', True,
     'A small aromatic herb with tiny leaves, part of the mint family. Wild thyme is the '
     'main ingredient of the famous za\'atar mix.',
     'Za\'atar, seasoning for meat and vegetables, herbal tea and natural remedies.'),
    ('Parsley', 'Parsley', 'herb', True,
     'A bright green biennial herb native to the central Mediterranean, with flat or curly leaves.',
     'Tabbouleh, garnishes, sauces, soups and salads.'),
    ('Lavender', 'Lavandula', 'herb', False,
     'A flowering plant of the mint family famous for its purple flower spikes and calming scent. '
     'Native to the Mediterranean and Middle East.',
     'Perfumes, essential oils, soaps, sachets and ornamental gardens.'),

    # --- More flowers ---
    ('Arabian Jasmine', 'Jasminum_sambac', 'flower', False,
     'A climbing shrub with small, white, very fragrant flowers that bloom at night. '
     'It is the national flower of the Philippines and loved across the Gulf.',
     'Perfumes, jasmine tea, garlands and decorating gardens.'),
    ('Tulip', 'Tulip', 'flower', False,
     'A spring-blooming bulb plant with large, cup-shaped colorful flowers. Wild tulips '
     'come from Central Asia; the Netherlands made them famous.',
     'Ornamental gardens, cut flowers and bouquets.'),
    ('Hibiscus', 'Hibiscus', 'flower', True,
     'A tropical flowering plant with large, showy trumpet-shaped flowers in red, pink, '
     'yellow and white.',
     'Hibiscus tea (karkadeh), natural food coloring, and ornamental hedges.'),
    ('Moth Orchid', 'Phalaenopsis', 'flower', False,
     'One of the most popular houseplant orchids, with long-lasting flowers shaped like moths in flight. '
     'Native to Southeast Asia.',
     'Indoor decoration, gifts and flower arrangements.'),

    # --- More succulents ---
    ('Prickly Pear', 'Opuntia', 'succulent', True,
     'A cactus with flat, paddle-shaped pads covered in spines. It produces sweet, '
     'colorful fruits known as "tin shoki".',
     'Fruit eaten fresh or in juices, young pads cooked as a vegetable, and natural fencing.'),
    ('Jade Plant', 'Crassula_ovata', 'succulent', False,
     'A succulent with thick, shiny, oval leaves and woody stems, native to South Africa. '
     'Easy to grow and can live for decades.',
     'Popular houseplant, bonsai, and believed to bring good luck.'),
    ('Snake Plant', 'Dracaena_trifasciata', 'succulent', False,
     'A hardy plant with stiff, upright, sword-shaped leaves, native to tropical West Africa. '
     'It survives low light and little water.',
     'Indoor decoration and one of the easiest houseplants for beginners.'),
]

# Where each plant comes from (shown as "Native to" on the detail page).
NATIVE_TO = {
    'Date Palm': 'Iraq, Saudi Arabia, Egypt',
    'Olive Tree': 'Mediterranean Basin (Syria, Lebanon, Greece)',
    'Oak': 'Europe, Asia, North America',
    'Mango': 'India, Bangladesh, Myanmar',
    'Pomegranate': 'Iran, Afghanistan, Northern India',
    'Strawberry': 'Hybrid of North & South American species (bred in France)',
    'Tomato': 'Peru, Ecuador',
    'Carrot': 'Iran, Afghanistan, Europe',
    'Spinach': 'Iran, Central Asia',
    'Mint': 'Europe, Asia, North Africa',
    'Basil': 'India, Tropical Africa, Southeast Asia',
    'Rose': 'Asia, Europe, North America',
    'Sunflower': 'North America (USA, Mexico)',
    'Aloe Vera': 'Arabian Peninsula (Oman, Yemen)',
    'Echeveria': 'Mexico, Central America',
    'Ghaf Tree': 'UAE, Oman, Saudi Arabia, Iran, India',
    'Sidr Tree': 'Saudi Arabia, Sudan, Egypt, Palestine',
    'Neem Tree': 'India, Pakistan, Bangladesh',
    'Fig': 'Western Asia, Middle East',
    'Lemon': 'Northeast India, Myanmar, China',
    'Banana': 'Southeast Asia, Papua New Guinea',
    'Grape': 'Caucasus, Mediterranean, Central Asia',
    'Watermelon': 'Sudan, Northeast Africa',
    'Potato': 'Peru, Bolivia (Andes)',
    'Cucumber': 'India',
    'Eggplant': 'India, Southeast Asia',
    'Rosemary': 'Mediterranean (Spain, Italy, Morocco)',
    'Thyme': 'Mediterranean, Southern Europe',
    'Parsley': 'Italy, Greece, Algeria',
    'Lavender': 'Mediterranean, Middle East, India',
    'Arabian Jasmine': 'India, Bhutan, Southeast Asia',
    'Tulip': 'Kazakhstan, Turkey, Iran',
    'Hibiscus': 'Tropical Asia, Africa, Pacific Islands',
    'Moth Orchid': 'Philippines, Indonesia, Malaysia',
    'Prickly Pear': 'Mexico',
    'Jade Plant': 'South Africa, Mozambique',
    'Snake Plant': 'Nigeria, Congo (West Africa)',
}

# Hand-picked Featured / Quality photos from Wikimedia Commons (file titles).
PHOTOS = {
    'Date Palm': 'Mazafati dates - whole, halved and seed.jpg',
    'Olive Tree': 'Olives vertes, fruit entier et coupé.jpg',
    'Oak': 'Acorn of Mount Tabor oak (Quercus ithaburensis), Agios Sostis, Tinos, Greece julesvernex2.jpg',
    'Mango': 'Mangos - single and halved.jpg',
    'Pomegranate': 'Pomegranate fruit - whole and piece with arils.jpg',
    'Strawberry': 'Garden strawberry (Fragaria × ananassa) single2.jpg',
    'Tomato': 'Tomato je.jpg',
    'Carrot': 'Vegetable-Carrot-Bundle-wStalks.jpg',
    'Mint': 'Mint leaves (Mentha spicata).jpg',
    'Rose': 'Red rose with black background.jpg',
    'Sunflower': 'VallejoSunflower.jpg',
    'Aloe Vera': 'Aloe vera plantation IMGP0177.jpg',
    'Echeveria': 'Rosette of Echeveria from top.jpg',
    'Fig': 'Bowl of Figs.jpg',
    'Lemon': 'Lemon - whole and split.jpg',
    'Grape': 'Table grapes on white.jpg',
    'Watermelon': 'Watermelon yellow 2024 G1.jpg',
    'Thyme': 'Thyme-Bundle.jpg',
    'Parsley': 'Petersilie - Nahaufnahme.JPG',
    'Lavender': "Île d'Orléans 009.jpg",
    'Arabian Jasmine': 'ياسمين متفتح.jpg',
    'Tulip': 'Tulip (15268993144).jpg',
    'Hibiscus': 'Hibiscus petal.jpg',
    'Moth Orchid': 'Phalaenopsis Cultivar Mini 01.jpg',
    'Jade Plant': 'Crassula ovata white spots on leaves.jpg',
    'Ghaf Tree': 'Prosopis cineraria kz01.jpg',
    'Sidr Tree': 'Ziziphus spina-christi kz05.jpg',
    'Banana': 'Bananas white background DS.jpg',
    'Potato': 'Potato cv Dejima.jpg',
    'Rosemary': 'Rosmarinus officinalis. Romeu.jpg',
    'Snake Plant': 'Sansevieria sitting beautifully well.jpg',
    'Cucumber': 'Cucumber from Denmark.jpg',
    'Basil': 'Fresh green basil leaves (54986224214).jpg',
}

# Static images used by the home hero and the contact page.
STATIC_IMAGES = {
    'hero.jpg': 'Succulent_plant',
    'orchid.jpg': 'Phalaenopsis',
}


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def wikipedia_image(article, width=960):
    """Return image bytes for the lead image of a Wikipedia article."""
    summary_url = 'https://en.wikipedia.org/api/rest_v1/page/summary/' + urllib.parse.quote(article)
    data = json.loads(fetch(summary_url))
    original = data.get('originalimage', {})
    thumb = data.get('thumbnail', {}).get('source')
    if thumb and original.get('width', 0) > width:
        try:
            return fetch(re.sub(r'/\d+px-', f'/{width}px-', thumb))
        except Exception:
            pass
    if original.get('source'):
        return fetch(original['source'])
    raise ValueError(f'No image found for {article}')


def commons_image(file_title, width=1280):
    """Return a resized copy of a Wikimedia Commons file (e.g. 'Mango on white.jpg')."""
    url = ('https://commons.wikimedia.org/wiki/Special:FilePath/'
           + urllib.parse.quote(file_title.replace(' ', '_')))
    try:
        return fetch(url + f'?width={width}')
    except Exception:
        # Thumbnail service busy: download the original and resize it locally.
        import io
        import time

        from PIL import Image
        time.sleep(5)
        img = Image.open(io.BytesIO(fetch(url))).convert('RGB')
        img.thumbnail((width, width * 2))
        buf = io.BytesIO()
        img.save(buf, 'JPEG', quality=88)
        return buf.getvalue()


def plant_image(name, article):
    """Hand-picked high-quality photo when we have one, else the Wikipedia lead image."""
    if name in PHOTOS:
        return commons_image(PHOTOS[name])
    return wikipedia_image(article)


class Command(BaseCommand):
    help = 'Add real plants (with high-quality photos) to the database.'

    def add_arguments(self, parser):
        parser.add_argument('--refresh-images', action='store_true',
                            help='Replace the photos of plants that already exist with the hand-picked ones.')

    def handle(self, *args, **options):
        static_dir = settings.BASE_DIR / 'static' / 'images'
        static_dir.mkdir(parents=True, exist_ok=True)
        for filename, article in STATIC_IMAGES.items():
            path = static_dir / filename
            if path.exists():
                continue
            try:
                path.write_bytes(wikipedia_image(article, width=1280))
                self.stdout.write(f'Saved static/images/{filename}')
            except Exception as exc:
                self.stderr.write(f'Could not get {filename}: {exc}')

        for name, article, category, is_edible, about, used_for in PLANTS:
            slug = name.lower().replace(' ', '-')
            plant = Plant.objects.filter(name=name).first()
            if plant and not plant.native_to and name in NATIVE_TO:
                plant.native_to = NATIVE_TO[name]
                plant.save(update_fields=['native_to'])
            if plant and not (options['refresh_images'] and name in PHOTOS):
                self.stdout.write(f'Skip {name} (exists)')
                continue
            try:
                image_bytes = plant_image(name, article)
            except Exception as exc:
                self.stderr.write(f'Could not get image for {name}: {exc}')
                continue
            if plant:
                plant.image.delete(save=False)
                plant.image.save(f'{slug}.jpg', ContentFile(image_bytes), save=True)
                self.stdout.write(self.style.SUCCESS(f'New photo for {name}'))
                continue
            plant = Plant(name=name, about=about, used_for=used_for, category=category,
                          is_edible=is_edible, native_to=NATIVE_TO.get(name, ''))
            plant.image.save(f'{slug}.jpg', ContentFile(image_bytes), save=False)
            plant.save()
            self.stdout.write(self.style.SUCCESS(f'Added {name}'))
