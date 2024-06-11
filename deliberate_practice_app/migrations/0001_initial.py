# Generated by Django 5.0.6 on 2024-06-11 18:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="PracticeSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField(auto_now_add=True)),
                ("end_time", models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="PracticeSet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "score",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "I wasn’t successful"),
                            (1, "I was ~25% successful"),
                            (2, "I was ~50% successful"),
                            (3, "I was ~75% successful"),
                            (4, "I executed the task flawlessly"),
                        ]
                    ),
                ),
                ("practice_time", models.DateTimeField(auto_now_add=True)),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="deliberate_practice_app.activity",
                    ),
                ),
                (
                    "practice_session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="practice_sets",
                        to="deliberate_practice_app.practicesession",
                    ),
                ),
            ],
        ),
    ]
