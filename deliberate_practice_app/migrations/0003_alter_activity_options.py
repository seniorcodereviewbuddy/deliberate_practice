# Generated by Django 5.0.6 on 2024-06-19 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("deliberate_practice_app", "0002_alter_activity_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="activity",
            options={"verbose_name": "Activity", "verbose_name_plural": "Activities"},
        ),
    ]
