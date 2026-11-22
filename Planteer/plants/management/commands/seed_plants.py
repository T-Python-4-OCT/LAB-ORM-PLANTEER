"""Fill the database with 20 real plants and their real photos.

    python manage.py seed_plants              # add the plants with their photos
    python manage.py seed_plants --no-images  # add the plants only (placeholder photo)

The photos are stored inside the project (plants/seed_images/), so no internet is needed.
They come from Wikimedia Commons — see each file's page for its author and license:
https://commons.wikimedia.org/wiki/File:<file name>  (file names are listed below).
Running the command again is safe: plants are never duplicated, and plants that still
use the placeholder get their photo.
"""
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from plants.models import Plant

SEED_IMAGES = Path(__file__).resolve().parents[2] / "seed_images"   # plants/seed_images/
DEFAULT_IMAGE = Plant._meta.get_field("image").default

T, FR, V, H, FL, S = (Plant.Category.TREE, Plant.Category.FRUIT, Plant.Category.VEGETABLE,
                      Plant.Category.HERB, Plant.Category.FLOWER, Plant.Category.SUCCULENT)

# name, category, is_edible, Wikimedia Commons photo (credit), about, used_for
# the photo file in seed_images/ is named after the plant: slugify(name) + ".jpg"
PLANTS = [
    # ---- Trees ----
    ("Neem", T, False, "Neem_Tree_in_Rajasthan,_India.jpg",
     "Azadirachta indica is a fast-growing evergreen tree from India with a wide, shady crown. "
     "It handles heat and drought very well and is planted along streets across hot countries, including Saudi Arabia.",
     "Its leaves, bark and seed oil are used in natural insect repellents, soaps and toothpaste; "
     "neem twigs were traditionally chewed to clean the teeth."),
    ("Baobab", T, True, "Baobab_and_elephant,_Tanzania.jpg",
     "Adansonia digitata is an African giant with a huge, bottle-shaped trunk that stores water for the dry season. "
     "Some baobabs are more than a thousand years old.",
     "The dry, tangy fruit pulp is rich in vitamin C and used in drinks and powders; "
     "the leaves are cooked as a vegetable and the bark fibre is made into rope."),
    ("Sidr", T, True, "Ziziphus-areva-israel.jpg",
     "Ziziphus spina-christi (Christ's thorn jujube) is a thorny, drought-tolerant tree native to Arabia "
     "and the Middle East, with small round fruits called nabk.",
     "Its flowers give the famous Sidr honey; the fruits are eaten fresh or dried, "
     "and the crushed leaves are traditionally used to wash the hair and body."),
    # ---- Fruits ----
    ("Mango", FR, True, "Mangos_-_single_and_halved.jpg",
     "Mangifera indica is a tropical tree from South Asia with sweet, juicy stone fruits. "
     "There are hundreds of varieties, from green to red and golden yellow.",
     "Eaten fresh, in juices, smoothies, desserts and ice cream; green mangoes are used in pickles and chutneys."),
    ("Guava", FR, True, "Guava_pink_fruit.jpg",
     "Psidium guajava is a small tropical tree with round fruits that have a strong, sweet smell "
     "and pink or white flesh full of small seeds.",
     "Eaten fresh or made into juice, jam and jelly; guava has more vitamin C than an orange."),
    ("Dragon Fruit", FR, True, "Pitaya_cross_section_ed2.jpg",
     "Pitaya comes from a climbing cactus (Selenicereus undatus). Its bright pink fruit with green scales "
     "hides white flesh dotted with tiny black seeds. The large flowers open only at night.",
     "Eaten fresh, in fruit salads, smoothie bowls and drinks; it is light, refreshing and full of fibre."),
    ("Papaya", FR, True, "Papaya_cross_section_BNC.jpg",
     "Carica papaya is a fast-growing tropical plant that looks like a tree with a single stem. "
     "Its orange fruit has a hollow center full of black seeds.",
     "Eaten fresh or in juices and salads; green papaya is cooked or shredded into salads, "
     "and its enzyme (papain) is used to tenderize meat."),
    # ---- Vegetables ----
    ("Okra", V, True, "Hong_Kong_Okra_Aug_25_2012.JPG",
     "Abelmoschus esculentus is a warm-season plant from the hibiscus family that grows long green pods. "
     "It loves heat, which makes it a popular summer crop in the Gulf.",
     "The young pods are cooked in stews such as bamya with meat and tomato, or fried and grilled."),
    ("Bell Pepper", V, True, "Green-Yellow-Red-Pepper-2009.jpg",
     "Capsicum annuum bell peppers are sweet, crunchy and not spicy. Green peppers are picked early; "
     "left on the plant, they turn yellow, orange or red and become sweeter.",
     "Salads, stir-fries, pizza, grilling and stuffing; peppers are very rich in vitamin C."),
    ("Broccoli", V, True, "Broccoli_and_cross_section_edit.jpg",
     "Brassica oleracea var. italica is a cool-season vegetable grown for its green head of tiny flower buds, "
     "picked before they open.",
     "Steamed, roasted, in soups and stir-fries, or raw in salads; packed with fibre and vitamins C and K."),
    # ---- Herbs ----
    ("Thyme", H, True, "Thyme-Bundle.jpg",
     "Thymus vulgaris is a small, woody herb with tiny fragrant leaves. It loves sun and dry soil "
     "and needs very little water.",
     "Seasoning meat, soups and roasted vegetables, and in herbal tea; it is a relative of the za'atar plants."),
    ("Parsley", H, True, "Petroselinum.jpg",
     "Petroselinum crispum is a bright green herb with flat or curly leaves. It grows easily in pots "
     "and is usually harvested before it flowers.",
     "The main herb in tabbouleh, and used fresh in salads, sauces and as a garnish; rich in vitamins A, C and K."),
    ("Lemongrass", H, True, "Gardenology.org-IMG_2892_rbgs11jan.jpg",
     "Cymbopogon citratus is a tall tropical grass that grows in thick clumps and smells strongly of lemon "
     "when its leaves are crushed.",
     "Teas, soups and curries in Thai and Vietnamese cooking; its oil is used in soaps and insect repellents."),
    ("Sage", H, True, "Salvia_officinalis0.jpg",
     "Salvia officinalis is a woody herb with soft grey-green leaves and purple flowers that attract bees. "
     "It likes sun and well-drained soil.",
     "A popular herbal tea (maramiya) in the Arab world, and used to season meat, stuffing and butter sauces."),
    # ---- Flowers ----
    ("Hibiscus", FL, True, "Hibiscus_Brilliant.jpg",
     "Hibiscus rosa-sinensis is a tropical shrub with large, bright flowers in red, pink, orange or yellow. "
     "Each flower lasts only a day or two, but the plant keeps blooming.",
     "Planted for hedges and garden color; the dried flowers of its relative (karkadeh) make a famous red tea."),
    ("Bougainvillea", FL, False, "Bougainvillea_closeup.jpg",
     "A thorny climbing shrub from South America. Its colorful 'petals' are actually papery leaves (bracts) "
     "around tiny white flowers. It thrives in heat and full sun.",
     "Covering walls, fences and pergolas with color — a very common sight in Saudi gardens and streets."),
    ("Arabian Jasmine", FL, True, "Jasmine_flower_(Jasminum_sambac).jpg",
     "Jasminum sambac is an evergreen climbing shrub with small, white, very fragrant flowers "
     "that open in the evening.",
     "Perfumes, garlands and flower necklaces; the flowers are used to scent jasmine tea. "
     "It is the national flower of the Philippines."),
    # ---- Succulents ----
    ("Echeveria", S, False, "Echeveria_elegans_-_1.jpg",
     "Echeveria elegans forms neat rosettes of pale blue-green leaves that look like stone roses. "
     "It stores water in its leaves and needs lots of light.",
     "A favourite in pots, rock gardens and succulent arrangements; new plants grow easily from a single leaf."),
    ("Agave", S, False, "Agave_americana_1.jpg",
     "Agave americana (century plant) grows a big rosette of thick, spiny leaves. After many years it sends up "
     "one tall flower stalk, and then the main plant dies.",
     "Landscaping in dry gardens; other agave species give agave syrup and the fibre sisal."),
    ("Golden Barrel Cactus", S, False, "Echinocactus_grusonii_2.jpg",
     "Echinocactus grusonii is a round cactus covered in golden-yellow spines, native to Mexico. "
     "It grows slowly and can live for decades.",
     "Desert landscaping and indoor pots; one of the easiest cacti for beginners. Handle it with care — the spines are sharp."),
]


class Command(BaseCommand):
    help = "Add 20 real plants with real photos (from plants/seed_images/) to the database."

    def add_arguments(self, parser):
        parser.add_argument("--no-images", action="store_true", help="Don't attach photos (use the placeholder).")

    def handle(self, *args, **options):
        created_count = photo_count = 0
        for name, category, is_edible, commons_file, about, used_for in PLANTS:
            plant, created = Plant.objects.get_or_create(
                name=name,
                defaults={"category": category, "is_edible": is_edible, "about": about, "used_for": used_for},
            )
            created_count += created
            status = "added" if created else "exists"

            photo = SEED_IMAGES / f"{slugify(name)}.jpg"
            if not options["no_images"] and plant.image.name == DEFAULT_IMAGE and photo.exists():
                with photo.open("rb") as f:
                    plant.image.save(photo.name, File(f), save=True)  # copied to media/plants/
                photo_count += 1
                status += " + photo"

            self.stdout.write(f"  • {name}: {status}")

        self.stdout.write(self.style.SUCCESS(
            f"Done — {created_count} new plant(s), {photo_count} photo(s) attached, "
            f"{Plant.objects.count()} plant(s) in the database."))
