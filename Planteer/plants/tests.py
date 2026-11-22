import io
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Comment, Plant

MEDIA = tempfile.mkdtemp()


def make_image(name="plant.png"):
    buf = io.BytesIO()
    Image.new("RGB", (40, 30), "green").save(buf, format="PNG")
    return SimpleUploadedFile(name, buf.getvalue(), content_type="image/png")


def plant(name="Mint", category=Plant.Category.HERB, is_edible=True, about="A herb.", used_for="Tea."):
    return Plant.objects.create(name=name, category=category, is_edible=is_edible, about=about, used_for=used_for)


@override_settings(MEDIA_ROOT=MEDIA)
class PlantPagesTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA, ignore_errors=True)

    def setUp(self):
        self.mint = plant("Mint", Plant.Category.HERB, True)
        self.basil = plant("Basil", Plant.Category.HERB, True)
        self.orchid = plant("Moth Orchid", Plant.Category.FLOWER, False, about="A houseplant.", used_for="Decoration.")

    # ---------- all plants + filters ----------
    def test_all_plants_lists_everything(self):
        res = self.client.get(reverse("plants:all_plants"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["plants"]), 3)

    def test_filter_by_category(self):
        res = self.client.get(reverse("plants:all_plants"), {"category": "herb"})
        self.assertEqual({p.name for p in res.context["plants"]}, {"Mint", "Basil"})

    def test_filter_by_is_edible(self):
        res = self.client.get(reverse("plants:all_plants"), {"is_edible": "no"})
        self.assertEqual([p.name for p in res.context["plants"]], ["Moth Orchid"])

    def test_filter_by_category_and_is_edible(self):
        res = self.client.get(reverse("plants:all_plants"), {"category": "flower", "is_edible": "yes"})
        self.assertEqual(len(res.context["plants"]), 0)
        self.assertContains(res, "No plants found")

    def test_unknown_filter_values_are_ignored(self):
        res = self.client.get(reverse("plants:all_plants"), {"category": "xyz", "is_edible": "maybe"})
        self.assertEqual(len(res.context["plants"]), 3)

    # ---------- detail + related plants ----------
    def test_detail_page(self):
        res = self.client.get(reverse("plants:plant_detail", args=[self.mint.id]))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Mint")
        self.assertContains(res, reverse("plants:update_plant", args=[self.mint.id]))
        self.assertContains(res, reverse("plants:delete_plant", args=[self.mint.id]))

    def test_related_plants_same_category_without_itself(self):
        res = self.client.get(reverse("plants:plant_detail", args=[self.mint.id]))
        self.assertEqual([p.name for p in res.context["related_plants"]], ["Basil"])

    def test_detail_404(self):
        self.assertEqual(self.client.get(reverse("plants:plant_detail", args=[999])).status_code, 404)

    # ---------- add / update / delete ----------
    def test_add_plant_with_image(self):
        res = self.client.post(reverse("plants:add_plant"), {
            "name": "Lavender", "category": "flower", "is_edible": "on",
            "about": "Purple flowers.", "used_for": "Oil.", "image": make_image(),
        })
        new = Plant.objects.get(name="Lavender")
        self.assertRedirects(res, reverse("plants:plant_detail", args=[new.id]))
        self.assertTrue(new.is_edible)
        self.assertTrue(new.image.name.startswith("plants/"))

    def test_add_plant_invalid(self):
        res = self.client.post(reverse("plants:add_plant"), {"name": "", "category": "herb", "about": "", "used_for": ""})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Give the plant a name.")
        self.assertEqual(Plant.objects.count(), 3)

    def test_update_form_prefilled_and_saves(self):
        url = reverse("plants:update_plant", args=[self.mint.id])
        self.assertContains(self.client.get(url), 'value="Mint"')
        res = self.client.post(url, {"name": "Spearmint", "category": "herb", "is_edible": "on",
                                     "about": "Fresh.", "used_for": "Tea."})
        self.assertRedirects(res, reverse("plants:plant_detail", args=[self.mint.id]))
        self.mint.refresh_from_db()
        self.assertEqual(self.mint.name, "Spearmint")
        self.assertEqual(Plant.objects.count(), 3)  # updated, not duplicated

    def test_delete_needs_post_and_removes_comments(self):
        Comment.objects.create(plant=self.mint, full_name="Sara", content="Nice")
        url = reverse("plants:delete_plant", args=[self.mint.id])
        self.assertContains(self.client.get(url), "Delete this plant?")
        self.assertTrue(Plant.objects.filter(pk=self.mint.pk).exists())
        res = self.client.post(url)
        self.assertRedirects(res, reverse("plants:all_plants"))
        self.assertFalse(Plant.objects.filter(pk=self.mint.pk).exists())
        self.assertEqual(Comment.objects.count(), 0)  # CASCADE

    # ---------- search ----------
    def test_search_by_name_and_about(self):
        res = self.client.get(reverse("plants:search"), {"q": "mint"})
        self.assertEqual([p.name for p in res.context["results"]], ["Mint"])
        res = self.client.get(reverse("plants:search"), {"q": "houseplant"})
        self.assertEqual([p.name for p in res.context["results"]], ["Moth Orchid"])

    def test_search_without_query_and_no_results(self):
        self.assertEqual(len(self.client.get(reverse("plants:search")).context["results"]), 0)
        self.assertContains(self.client.get(reverse("plants:search"), {"q": "zzz"}), "No plants found")


class CommentTests(TestCase):
    def setUp(self):
        self.mint = plant("Mint")
        self.basil = plant("Basil")
        self.url = reverse("plants:add_comment", args=[self.mint.id])

    def test_many_comments_belong_to_one_plant(self):
        c = Comment.objects.create(plant=self.mint, full_name="Sara", content="Great for tea")
        Comment.objects.create(plant=self.mint, full_name="Omar", content="Grows fast")
        Comment.objects.create(plant=self.basil, full_name="Lina", content="Pesto!")
        self.assertEqual(c.plant_id, self.mint.id)   # foreign key -> plant's primary key
        self.assertEqual(self.mint.comments.count(), 2)

    def test_add_comment(self):
        res = self.client.post(self.url, {"full_name": "Sara Ahmed", "content": "I grow it on my balcony."})
        self.assertRedirects(res, reverse("plants:plant_detail", args=[self.mint.id]) + "#comments",
                             fetch_redirect_response=False)
        comment = Comment.objects.get()
        self.assertEqual(comment.plant, self.mint)
        self.assertIsNotNone(comment.created_at)
        self.assertContains(self.client.get(reverse("plants:plant_detail", args=[self.mint.id])), "I grow it on my balcony.")

    def test_invalid_comment(self):
        res = self.client.post(self.url, {"full_name": "", "content": ""})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Write your name.")
        self.assertEqual(Comment.objects.count(), 0)

    def test_get_add_comment_redirects(self):
        self.assertRedirects(self.client.get(self.url), reverse("plants:plant_detail", args=[self.mint.id]))


@override_settings(MEDIA_ROOT=MEDIA)
class SeedCommandTests(TestCase):
    def test_every_seed_plant_has_its_photo_file(self):
        from django.utils.text import slugify
        from plants.management.commands.seed_plants import PLANTS, SEED_IMAGES
        for name, *_ in PLANTS:
            self.assertTrue((SEED_IMAGES / f"{slugify(name)}.jpg").exists(), name)

    def test_seed_adds_plants_with_photos_once(self):
        call_command("seed_plants", stdout=io.StringIO())
        self.assertEqual(Plant.objects.count(), 20)
        self.assertTrue(Plant.objects.get(name="Mango").image.name.startswith("plants/mango"))
        self.assertFalse(Plant.objects.filter(image="plants/default.jpg").exists())
        call_command("seed_plants", stdout=io.StringIO())  # no duplicates
        self.assertEqual(Plant.objects.count(), 20)
        for category, _ in Plant.Category.choices:  # every category has at least 3 plants
            self.assertGreaterEqual(Plant.objects.filter(category=category).count(), 3)

    def test_seed_without_images_uses_placeholder(self):
        call_command("seed_plants", "--no-images", stdout=io.StringIO())
        self.assertEqual(Plant.objects.get(name="Hibiscus").image.name, "plants/default.jpg")
