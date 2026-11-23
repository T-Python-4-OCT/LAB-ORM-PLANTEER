import shutil
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Comment, Plant


def make_plant(name="Mint", category=Plant.Category.HERB, is_edible=True):
    """Helper: create a plant quickly inside tests."""
    return Plant.objects.create(
        name=name,
        about=f"About {name}",
        used_for="Cooking",
        image="plants/test.jpg",
        category=category,
        is_edible=is_edible,
    )


def make_image_file(name="test.jpg"):
    """Helper: a tiny real JPEG image for upload tests."""
    buffer = BytesIO()
    Image.new("RGB", (10, 10), "green").save(buffer, format="JPEG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")


# Uploaded test images go to a temporary folder, not the real media/ folder
TEMP_MEDIA = tempfile.mkdtemp()


class PlantModelTests(TestCase):
    def test_str_returns_name(self):
        self.assertEqual(str(make_plant(name="Basil")), "Basil")

    def test_comments_related_name_and_cascade(self):
        plant = make_plant()
        Comment.objects.create(plant=plant, full_name="Sara Ali", content="Lovely!")
        self.assertEqual(plant.comments.count(), 1)

        plant.delete()  # CASCADE should delete the comment too
        self.assertEqual(Comment.objects.count(), 0)


class PlantDetailTests(TestCase):
    def test_detail_page_loads(self):
        plant = make_plant(name="Olive Tree", category=Plant.Category.TREE)
        response = self.client.get(reverse("plants:plant_detail", args=[plant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Olive Tree")

    def test_detail_page_404_for_missing_plant(self):
        response = self.client.get(reverse("plants:plant_detail", args=[999]))
        self.assertEqual(response.status_code, 404)


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class PlantCrudTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)
        super().tearDownClass()

    def valid_data(self, **changes):
        data = {
            "name": "Lavender",
            "category": Plant.Category.FLOWER,
            "is_edible": "on",
            "about": "A fragrant purple flower.",
            "used_for": "Perfumes and tea.",
        }
        data.update(changes)
        return data

    # ----- Create -----
    def test_add_page_loads(self):
        response = self.client.get(reverse("plants:plant_create"))
        self.assertEqual(response.status_code, 200)

    def test_add_plant_with_valid_data(self):
        data = self.valid_data(image=make_image_file())
        response = self.client.post(reverse("plants:plant_create"), data, follow=True)

        plant = Plant.objects.get(name="Lavender")
        self.assertTrue(plant.is_edible)
        self.assertTrue(plant.image.name.startswith("plants/"))
        self.assertRedirects(response, reverse("plants:plant_detail", args=[plant.id]))
        self.assertContains(response, "was added successfully")

    def test_add_plant_rejects_empty_form(self):
        response = self.client.post(reverse("plants:plant_create"), {})
        self.assertEqual(response.status_code, 200)  # form shown again with errors
        self.assertEqual(Plant.objects.count(), 0)
        self.assertTrue(response.context["form"].errors)

    def test_add_plant_requires_image(self):
        self.client.post(reverse("plants:plant_create"), self.valid_data())
        self.assertEqual(Plant.objects.count(), 0)

    # ----- Update -----
    def test_update_page_is_prefilled(self):
        plant = make_plant(name="Mint")
        response = self.client.get(reverse("plants:plant_update", args=[plant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].instance, plant)

    def test_update_plant_keeps_old_image(self):
        plant = make_plant(name="Mint")
        data = self.valid_data(name="Peppermint", category=Plant.Category.HERB)
        response = self.client.post(reverse("plants:plant_update", args=[plant.id]), data)

        plant.refresh_from_db()
        self.assertEqual(plant.name, "Peppermint")
        self.assertEqual(plant.image.name, "plants/test.jpg")  # not removed
        self.assertRedirects(response, reverse("plants:plant_detail", args=[plant.id]))

    def test_update_missing_plant_returns_404(self):
        response = self.client.get(reverse("plants:plant_update", args=[999]))
        self.assertEqual(response.status_code, 404)

    # ----- Delete -----
    def test_delete_get_shows_confirmation_and_does_not_delete(self):
        plant = make_plant()
        response = self.client.get(reverse("plants:plant_delete", args=[plant.id]))
        self.assertContains(response, "Delete Mint?")
        self.assertTrue(Plant.objects.filter(pk=plant.id).exists())

    def test_delete_post_deletes_plant(self):
        plant = make_plant()
        response = self.client.post(reverse("plants:plant_delete", args=[plant.id]))
        self.assertRedirects(response, reverse("main:home"))
        self.assertFalse(Plant.objects.filter(pk=plant.id).exists())


class AllPlantsFilterTests(TestCase):
    def setUp(self):
        self.mint = make_plant(name="Mint", category=Plant.Category.HERB, is_edible=True)
        self.olive = make_plant(name="Olive Tree", category=Plant.Category.TREE, is_edible=True)
        self.neem = make_plant(name="Neem Tree", category=Plant.Category.TREE, is_edible=False)
        self.url = reverse("plants:all_plants")

    def names(self, response):
        return {plant.name for plant in response.context["plants"]}

    def test_all_plants_page_lists_every_plant(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.names(response), {"Mint", "Olive Tree", "Neem Tree"})

    def test_filter_by_category(self):
        response = self.client.get(self.url, {"category": "tree"})
        self.assertEqual(self.names(response), {"Olive Tree", "Neem Tree"})

    def test_filter_by_edible(self):
        self.assertEqual(self.names(self.client.get(self.url, {"is_edible": "yes"})), {"Mint", "Olive Tree"})
        self.assertEqual(self.names(self.client.get(self.url, {"is_edible": "no"})), {"Neem Tree"})

    def test_filters_work_together(self):
        response = self.client.get(self.url, {"category": "tree", "is_edible": "no"})
        self.assertEqual(self.names(response), {"Neem Tree"})

    def test_selected_filters_are_kept_in_the_form(self):
        response = self.client.get(self.url, {"category": "tree", "is_edible": "no"})
        self.assertContains(response, '<option value="tree" selected>')
        self.assertContains(response, '<option value="no" selected>')

    def test_invalid_filter_values_are_ignored(self):
        response = self.client.get(self.url, {"category": "rocks", "is_edible": "maybe"})
        self.assertEqual(len(response.context["plants"]), 3)

    def test_no_match_shows_empty_message(self):
        response = self.client.get(self.url, {"category": "flower"})
        self.assertContains(response, "No plants match these filters")


class SearchTests(TestCase):
    def setUp(self):
        make_plant(name="Date Palm", category=Plant.Category.TREE)
        Plant.objects.create(name="Basil", about="A fragrant herb for pesto.", used_for="Cooking", image="plants/x.jpg")
        self.url = reverse("plants:search")

    def test_search_page_loads_without_query(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Type a plant name to start")

    def test_search_by_name_is_case_insensitive(self):
        response = self.client.get(self.url, {"q": "palm"})
        self.assertEqual([p.name for p in response.context["results"]], ["Date Palm"])

    def test_search_by_description(self):
        response = self.client.get(self.url, {"q": "pesto"})
        self.assertEqual([p.name for p in response.context["results"]], ["Basil"])

    def test_search_term_is_kept_in_input(self):
        response = self.client.get(self.url, {"q": "palm"})
        self.assertContains(response, 'value="palm"')

    def test_search_with_no_results(self):
        response = self.client.get(self.url, {"q": "cactus"})
        self.assertContains(response, 'No plants found for "cactus"')


class CommentTests(TestCase):
    def setUp(self):
        self.plant = make_plant(name="Mint")
        self.other_plant = make_plant(name="Basil")
        self.url = reverse("plants:plant_detail", args=[self.plant.id])

    def test_detail_page_shows_comment_form(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Post comment")
        self.assertIn("comment_form", response.context)

    def test_visitor_can_add_comment_without_login(self):
        data = {"full_name": "Sara Ali", "content": "Great in tea!"}
        response = self.client.post(self.url, data, follow=True)

        comment = Comment.objects.get()
        self.assertEqual(comment.plant, self.plant)  # linked to the right plant
        self.assertRedirects(response, self.url + "#comments")
        self.assertContains(response, "Your comment was posted")
        self.assertContains(response, "Great in tea!")

    def test_empty_comment_is_rejected(self):
        response = self.client.post(self.url, {"full_name": "", "content": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertTrue(response.context["comment_form"].errors)

    def test_whitespace_only_comment_is_rejected(self):
        self.client.post(self.url, {"full_name": "   ", "content": "   "})
        self.assertEqual(Comment.objects.count(), 0)

    def test_cannot_comment_on_missing_plant(self):
        url = reverse("plants:plant_detail", args=[999])
        response = self.client.post(url, {"full_name": "Sara", "content": "Hi"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Comment.objects.count(), 0)

    def test_page_only_shows_this_plants_comments(self):
        Comment.objects.create(plant=self.plant, full_name="A", content="About mint")
        Comment.objects.create(plant=self.other_plant, full_name="B", content="About basil")
        response = self.client.get(self.url)
        self.assertContains(response, "About mint")
        self.assertNotContains(response, "About basil")

    def test_comments_are_newest_first(self):
        old = Comment.objects.create(plant=self.plant, full_name="A", content="first")
        new = Comment.objects.create(plant=self.plant, full_name="B", content="second")
        response = self.client.get(self.url)
        self.assertEqual(list(response.context["comments"]), [new, old])


class RelatedPlantsTests(TestCase):
    def test_related_plants_have_same_category_and_exclude_current(self):
        olive = make_plant(name="Olive Tree", category=Plant.Category.TREE)
        palm = make_plant(name="Date Palm", category=Plant.Category.TREE)
        make_plant(name="Mint", category=Plant.Category.HERB)

        response = self.client.get(reverse("plants:plant_detail", args=[olive.id]))
        self.assertEqual(list(response.context["related_plants"]), [palm])

    def test_related_plants_are_limited_to_three(self):
        current = make_plant(name="Tree 0", category=Plant.Category.TREE)
        for i in range(1, 6):
            make_plant(name=f"Tree {i}", category=Plant.Category.TREE)
        response = self.client.get(reverse("plants:plant_detail", args=[current.id]))
        self.assertEqual(len(response.context["related_plants"]), 3)

    def test_message_when_no_related_plants(self):
        plant = make_plant(name="Lonely Rose", category=Plant.Category.FLOWER)
        response = self.client.get(reverse("plants:plant_detail", args=[plant.id]))
        self.assertContains(response, "No related plants yet")
