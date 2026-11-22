from django.core.management.base import BaseCommand
from plants.models import Plant

class Command(BaseCommand):
    help = 'Add the starter plant collection without duplicating existing plants.'

    def handle(self, *args, **options):
        plants = [
            ('Monstera deliciosa', 'Monstera deliciosa', 'indoor', False, 'photo-1501004318641-b39e6451bec6', 'Known for its dramatic split leaves, Monstera is a tropical climbing plant native to Central America. Give it room to climb and watch each new leaf reveal its own beautiful pattern.', 'A bold, leafy focal point for bright living spaces. Keep away from children and pets: the foliage is toxic if ingested.', 'Bright, indirect light', 'Water when the top 3–5 cm of soil dries'),
            ('Golden pothos', 'Epipremnum aureum', 'indoor', False, 'photo-1497250681960-ef046c08a56e', 'A forgiving tropical vine with heart-shaped leaves and golden variegation. Its trailing stems make it a lovely choice for shelves and hanging planters.', 'Trailing greenery for indoor spaces. Toxic if ingested; keep away from pets and children.', 'Medium to bright, indirect light', 'Let the top layer of soil dry between watering'),
            ('Aloe vera', 'Aloe barbadensis miller', 'succulent', False, 'photo-1596547609652-9cf5d8d76921', 'A sculptural succulent that stores water in thick, fleshy leaves. Aloe enjoys a sunny spot and a free-draining potting mix. It is happiest when you resist the urge to overwater.', 'An architectural accent for sunny windowsills. This collection treats aloe as ornamental; do not consume the plant.', 'Bright light with some direct sun', 'Water deeply only after the soil dries fully'),
            ('Sweet basil', 'Ocimum basilicum', 'herb', True, 'photo-1618375569909-3c8616cf7733', 'Sweet basil is an aromatic annual herb loved for its tender green leaves. Pinch out growing tips regularly to encourage a bushier plant, and harvest before flowering for the best flavor.', 'Fresh pesto, salads, pasta, and a fragrant kitchen garden. Wash leaves before culinary use.', 'At least 6 hours of sunlight', 'Keep evenly moist, never waterlogged'),
            ('Snake plant', 'Dracaena trifasciata', 'indoor', False, 'photo-1593482892290-f54927ae2b7a', 'Upright sword-shaped foliage gives this resilient plant a striking silhouette. Native to tropical West Africa, it tolerates a range of light conditions and prefers a light hand with watering.', 'Low-maintenance indoor greenery. Toxic if ingested; keep away from pets and children.', 'Indirect light; tolerates lower light', 'Allow soil to dry completely'),
            ('Echeveria', 'Echeveria elegans', 'succulent', False, 'photo-1459411552884-841db9b3cc2a', 'A rosette-forming succulent with pale, fleshy leaves. Echeveria needs plenty of light and gritty soil to keep its compact shape. Avoid leaving water sitting in the center of the rosette.', 'Sunny container gardens and small-space displays.', 'Bright light and gentle morning sun', 'Water the soil only when completely dry'),
            ('Rosemary', 'Salvia rosmarinus', 'herb', True, 'photo-1515586000433-45406d8e6662', 'This evergreen Mediterranean shrub carries aromatic, needle-like leaves. It thrives in sunshine and well-drained soil, bringing year-round texture and fragrance to a sunny balcony or garden.', 'Seasoning roasted vegetables, breads, and savory dishes. Wash sprigs before use.', 'Full sun, 6–8 hours a day', 'Allow soil to dry slightly between watering'),
            ('Moth orchid', 'Phalaenopsis', 'flowering', False, 'photo-1566907225472-2f5a93116a32', 'Moth orchids are tropical epiphytes with graceful arching flower spikes. Grow them in an airy orchid bark mix rather than dense soil, and keep their crown free of standing water.', 'Long-lasting indoor floral displays and thoughtful gifts.', 'Bright, indirect light; avoid hot direct sun', 'Water when the bark is nearly dry'),
        ]
        vegetables = [
            ('Tomato', 'Solanum lycopersicum', 1327838, 'A warm-season plant grown for its juicy fruits. Train the stems on a support and pick tomatoes as they ripen.', 'Fresh salads, sauces, and roasting. Eat ripe fruits; do not eat the leaves or stems.', 'Full sun, at least 6 hours', 'Water at the base; keep soil consistently moist'),
            ('Carrot', 'Daucus carota subsp. sativus', 143133, 'A root vegetable that grows best in loose, deep soil. Sow directly where it will grow and thin seedlings to give each root space.', 'Crunchy salads, soups, and roasted vegetables. Wash roots thoroughly before use.', 'Full sun to light partial shade', 'Keep the soil evenly moist during root development'),
            ('Broccoli', 'Brassica oleracea var. italica', 7676083, 'A cool-season vegetable grown for its compact green flower heads. Harvest the central head while the buds are still tightly closed.', 'Steaming, stir-fries, soups, and roasting. The florets and tender stems are edible.', 'Full sun, around 6 hours', 'Water regularly to keep soil evenly moist'),
            ('Bell pepper', 'Capsicum annuum', 594137, 'A warm-season vegetable with crisp, mild fruits. Grow in a sunny, sheltered spot and support branches as the peppers develop.', 'Fresh salads, stuffed peppers, grilling, and stir-fries. Remove the stem and wash before preparing.', 'Full sun, 6–8 hours', 'Water regularly and avoid letting the soil dry out fully'),
        ]
        for name, scientific, photo_id, about, used, light, water in vegetables:
            url = f'https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w=1400'
            plants.append((name, scientific, 'vegetable', True, url, about, used, light, water))
        corrected_photos = {
            'Monstera deliciosa': ('photo-1501004318641-b39e6451bec6', 6954409),
            'Golden pothos': ('photo-1497250681960-ef046c08a56e', 11838530),
            'Echeveria': ('photo-1459411552884-841db9b3cc2a', 16753186),
        }
        created = 0
        for name, scientific, category, edible, photo, about, used, light, water in plants:
            image_url = photo if photo.startswith('https://') else f'https://images.unsplash.com/{photo}?auto=format&fit=crop&w=900&q=85'
            correction = corrected_photos.get(name)
            if correction:
                photo_id = correction[1]
                image_url = f'https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w=1400'
            plant, added = Plant.objects.get_or_create(name=name, defaults={'scientific_name': scientific, 'category': category, 'is_edible': edible, 'image_url': image_url, 'about': about, 'used_for': used, 'light': light, 'water': water})
            if correction and not added and not plant.image and plant.image_url.startswith(f'https://images.unsplash.com/{correction[0]}?'):
                plant.image_url = image_url
                plant.save(update_fields=['image_url'])
            created += added
        self.stdout.write(self.style.SUCCESS(f'Added {created} plants. Collection has {Plant.objects.count()} plants.'))
