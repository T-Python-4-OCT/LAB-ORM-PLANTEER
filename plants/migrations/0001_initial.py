import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Plant",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=1024)),
                ("about", models.TextField()),
                ("used_for", models.TextField()),
                ("image", models.ImageField(upload_to="images/")),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("tree", "Tree"),
                            ("fruit", "Fruit"),
                            ("vegetables", "Vegetables"),
                            ("herb", "Herb"),
                            ("flower", "Flower"),
                            ("succulent", "Succulent"),
                        ],
                        max_length=64,
                    ),
                ),
                ("is_edible", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=1024)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "plant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="plants.plant",
                    ),
                ),
            ],
        ),
    ]
