# Generated by Django 4.2.5 on 2023-09-28 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
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
                    "line_1",
                    models.CharField(max_length=255, verbose_name="Address Line 1"),
                ),
                (
                    "line_2",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Address Line 2",
                    ),
                ),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                (
                    "postal_code",
                    models.CharField(max_length=20, verbose_name="Postal Code"),
                ),
                ("country", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="InventoryItem",
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
                ("name", models.CharField(max_length=255)),
                ("quantity", models.IntegerField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("batch_number", models.CharField(blank=True, max_length=20)),
                ("production_date", models.DateField(blank=True)),
                ("expiration_date", models.DateField(blank=True)),
                ("temperature", models.IntegerField(blank=True)),
                ("comment", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="StockItem",
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
                ("name", models.CharField(max_length=255)),
                (
                    "size",
                    models.FloatField(
                        choices=[
                            (0.5, "0.5 Litres"),
                            (3, "3 Litres "),
                            (6, "6 Litres "),
                        ]
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("production_date", models.DateField()),
                ("expiration_date", models.DateField()),
                ("comment", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="WorkingHours",
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
            ],
        ),
        migrations.CreateModel(
            name="StaffMember",
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
                ("name", models.CharField(max_length=255)),
                ("date_of_birth", models.DateField()),
                ("email", models.CharField(max_length=255)),
                ("phone", models.CharField()),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.address"
                    ),
                ),
            ],
        ),
    ]