from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Plant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                ("about", models.TextField()),
                ("used_for", models.TextField()),
                ("image", models.ImageField(upload_to="plants/")),
                (
                    "category",
                    models.CharField(
                        max_length=20,
                        choices=[
                            ("herb", "Herb"),
                            ("flower", "Flower"),
                            ("houseplant", "Houseplant"),
                            ("tree", "Tree"),
                            ("fruit", "Fruit"),
                            ("vegetable", "Vegetable"),
                        ],
                    ),
                ),
                ("is_edible", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at", "-pk"]},
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("full_name", models.CharField(max_length=120)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "plant",
                    models.ForeignKey(
                        to="plants.plant", related_name="comments", on_delete=models.CASCADE
                    ),
                ),
            ],
            options={"ordering": ["-created_at", "-pk"]},
        ),
    ]
