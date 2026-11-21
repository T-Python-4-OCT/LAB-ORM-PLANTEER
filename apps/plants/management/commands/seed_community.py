
import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.core.models import Contact
from apps.plants.models import Plant, Comment


DEMO_USERS = [
    ("ahmed_ali", "Ahmed", "Ali"),
    ("sara_khalid", "Sara", "Khalid"),
    ("mohammed_salem", "Mohammed", "Salem"),
    ("noura_fahad", "Noura", "Fahad"),
    ("khalid_omar", "Khalid", "Omar"),
    ("reem_abdullah", "Reem", "Abdullah"),
    ("faisal_hamad", "Faisal", "Hamad"),
    ("layan_saad", "Layan", "Saad"),
    ("abdullah_nasser", "Abdullah", "Nasser"),
    ("maha_ibrahim", "Maha", "Ibrahim"),
    ("omar_hassan", "Omar", "Hassan"),
    ("dana_yousef", "Dana", "Yousef"),
    ("yousef_ahmed", "Yousef", "Ahmed"),
    ("hessa_mohammed", "Hessa", "Mohammed"),
    ("saad_khalid", "Saad", "Khalid"),
    ("raghad_ali", "Raghad", "Ali"),
    ("ibrahim_salem", "Ibrahim", "Salem"),
    ("fatimah_omar", "Fatimah", "Omar"),
    ("bader_faisal", "Bader", "Faisal"),
    ("mariam_nasser", "Mariam", "Nasser"),
]


COMMENT_TEMPLATES = [
    "Beautiful plant! I really like the appearance of {plant}.",
    "I have been learning about {plant} recently. Very interesting!",
    "The photos of {plant} are amazing.",
    "Does anyone here grow {plant} at home?",
    "I would love to add {plant} to my garden.",
    "Thanks for sharing information about {plant}.",
    "This is one of my favorite plants!",
    "The details about {plant} are really helpful.",
    "I've seen this plant before but didn't know its name.",
    "Such a lovely example of {plant}!",
    "I like how the photos show the plant's details.",
    "What kind of soil works best for {plant}?",
    "Is {plant} suitable for growing indoors?",
    "I would love to learn more about caring for {plant}.",
    "Great addition to the Planteer collection!",
    "The colors and textures of this plant are beautiful.",
    "Does {plant} need frequent watering?",
    "I appreciate the information provided here.",
    "This photo makes me want to start gardening.",
    "I've been looking for information about {plant}.",
    "Can this plant grow in a hot climate?",
    "Very nice! I hope to see more photos of {plant}.",
    "This plant looks fascinating.",
    "I wonder how long {plant} takes to grow.",
    "Thanks! This was useful for my plant research.",
]


CONTACT_TEMPLATES = [
    "Hello! I really like Planteer. Keep up the great work!",
    "Can you add more information about plant care?",
    "It would be helpful to include watering instructions.",
    "I love the plant photo galleries. Nice work!",
    "Could you add information about soil requirements?",
    "I have a suggestion: add a favorites feature.",
    "The website is easy to navigate. Thank you!",
    "Could you include more indoor plants?",
    "I'd like to see a section about gardening tips.",
    "Can users upload more photos for each plant?",
    "The search feature is helpful. Great job!",
    "It would be nice to have a dark mode.",
    "Could you add more information about sunlight needs?",
    "I'd love to see plants suitable for Saudi Arabia.",
    "Can you add a guide for beginners?",
    "The categories are useful for exploring plants.",
    "I found the information about {plant} interesting.",
    "Could you include common plant diseases?",
    "Please add information about seasonal plant care.",
    "I would love a way to save my favorite plants.",
    "Thank you for building this plant database!",
    "Could you add Arabic language support?",
    "It would be useful to sort plants alphabetically.",
    "I like how the plants are organized.",
    "Can you include more photos of {plant}?",
]


class Command(BaseCommand):
    help = "Create demo users, plant comments, and contact messages."

    def handle(self, *args, **options):
        rng = random.Random(2026)
        User = get_user_model()

        plants = list(Plant.objects.all())

        if not plants:
            self.stderr.write(
                self.style.ERROR(
                    "No plants found. Run seed_plants first."
                )
            )
            return

        now = timezone.now()
        users = []
        users_created = 0
        comments_created = 0
        messages_created = 0

        # =============================
        # CREATE DEMO USERS
        # =============================

        for username, first_name, last_name in DEMO_USERS:
            demo_username = f"demo_{username}"
            demo_email = f"{demo_username}@example.com"

            user, created = User.objects.get_or_create(
                username=demo_username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": demo_email,
                    "is_staff": False,
                    "is_superuser": False,
                    "is_active": True,
                },
            )

            # Do not use or modify an unrelated account
            # that happens to have the same username.
            if user.email != demo_email:
                self.stderr.write(
                    f"SKIPPED username conflict: {demo_username}"
                )
                continue

            if created:
                user.set_unusable_password()
                user.save(update_fields=["password"])

                joined_at = now - timedelta(
                    days=rng.randint(15, 120)
                )

                User.objects.filter(pk=user.pk).update(
                    date_joined=joined_at
                )

                users_created += 1

            users.append(user)

        if not users:
            self.stderr.write(
                self.style.ERROR("No demo users available.")
            )
            return

        # =============================
        # CREATE PLANT COMMENTS
        # =============================

        comment_targets = [
            rng.choice(plants)
            for _ in range(80)
        ]

        for index, plant in enumerate(comment_targets):
            user = rng.choice(users)

            template = COMMENT_TEMPLATES[
                index % len(COMMENT_TEMPLATES)
            ]

            content = template.format(
                plant=plant.name
            )

            comment, created = Comment.objects.get_or_create(
                plant=plant,
                user=user,
                content=content,
            )

            if created:
                comment_date = now - timedelta(
                    days=rng.randint(0, 30),
                    hours=rng.randint(0, 23),
                    minutes=rng.randint(0, 59),
                )

                Comment.objects.filter(
                    pk=comment.pk
                ).update(
                    created_at=comment_date
                )

                comments_created += 1

        # =============================
        # CREATE CONTACT MESSAGES
        # =============================

        for index in range(35):
            user = users[index % len(users)]
            plant = rng.choice(plants)

            template = CONTACT_TEMPLATES[
                index % len(CONTACT_TEMPLATES)
            ]

            message_text = template.format(
                plant=plant.name
            )

            # Distinguish repeated demo submissions.
            if index >= len(CONTACT_TEMPLATES):
                message_text += (
                    f"\n\nI also enjoyed exploring {plant.name}."
                )

            contact, created = Contact.objects.get_or_create(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                message=message_text,
            )

            if created:
                message_date = now - timedelta(
                    days=rng.randint(0, 25),
                    hours=rng.randint(0, 23),
                )

                Contact.objects.filter(
                    pk=contact.pk
                ).update(
                    created_at=message_date
                )

                messages_created += 1

        # =============================
        # SUMMARY
        # =============================

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "COMMUNITY SEED COMPLETED!"
            )
        )

        self.stdout.write(
            f"New demo users: {users_created}"
        )

        self.stdout.write(
            f"New comments: {comments_created}"
        )

        self.stdout.write(
            f"New contact messages: {messages_created}"
        )

        self.stdout.write(
            f"Total users: {User.objects.count()}"
        )

        self.stdout.write(
            f"Total comments: {Comment.objects.count()}"
        )

        self.stdout.write(
            f"Total contact messages: {Contact.objects.count()}"
        )
