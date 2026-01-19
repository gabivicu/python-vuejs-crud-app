# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="category",
            field=models.CharField(
                choices=[
                    ("work", "Work"),
                    ("personal", "Personal"),
                    ("shopping", "Shopping"),
                    ("health", "Health"),
                    ("finance", "Finance"),
                    ("other", "Other"),
                ],
                default="other",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="priority",
            field=models.CharField(
                choices=[
                    ("low", "Low"),
                    ("medium", "Medium"),
                    ("high", "High"),
                    ("urgent", "Urgent"),
                ],
                default="medium",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="due_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="item",
            name="tags",
            field=models.CharField(
                blank=True, help_text="Comma-separated tags", max_length=500
            ),
        ),
    ]
