from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ManagerUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("username", models.CharField(max_length=30, unique=True)),
                ("email", models.EmailField(max_length=255, unique=True)),
                (
                    "is_staff",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user can access the admin site.",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="manager_users",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
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
            name="IceCreamProduction",
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
                    "container_size",
                    models.FloatField(
                        choices=[(0.5, "0.5 Litres"), (3, "3 Litres"), (6, "6 Litres")]
                    ),
                ),
                (
                    "quantity_produced",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("date_produced", models.DateTimeField(auto_now_add=True)),
                (
                    "produced_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ingredient",
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
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "unit_of_measurement",
                    models.CharField(
                        choices=[("grams", "Grams"), ("units", "Units")],
                        default="grams",
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Recipe",
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
                ("flavor", models.CharField(max_length=255, unique=True)),
                ("is_base", models.BooleanField(default=False)),
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
            name="UserProfile",
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
                ("is_manager", models.BooleanField(default=False)),
                ("is_service", models.BooleanField(default=False)),
                ("is_production", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
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
                (
                    "size",
                    models.FloatField(
                        choices=[(0.5, "0.5 Litres"), (3, "3 Litres"), (6, "6 Litres")],
                        default=0.5,
                    ),
                ),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)),
                ("date_added", models.DateTimeField(auto_now=True)),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.recipe",
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
                ("phone", models.CharField(max_length=255)),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("Service", "Service"),
                            ("Manager", "Manager"),
                            ("Production", "Production"),
                        ],
                        default="Service",
                        max_length=10,
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.address"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RecipeIngredient",
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
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.ingredient"
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.recipe"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                through="api.RecipeIngredient", to="api.ingredient"
            ),
        ),
        migrations.CreateModel(
            name="IngredientInventory",
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
                    "quantity",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                (
                    "ingredient_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.ingredient"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IngredientIncoming",
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
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "unit_of_measurement",
                    models.CharField(
                        choices=[("grams", "Grams"), ("units", "Units")],
                        default="grams",
                        max_length=10,
                    ),
                ),
                ("date_received", models.DateTimeField(auto_now_add=True)),
                ("lot_number", models.CharField(blank=True, max_length=255, null=True)),
                ("expiration_date", models.DateField(blank=True, null=True)),
                (
                    "temperature",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                ("observations", models.TextField(blank=True, null=True)),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.ingredient"
                    ),
                ),
                (
                    "received_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IceCreamStockTakeOut",
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
                    "quantity_moved",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("date_moved", models.DateTimeField()),
                (
                    "ice_cream_production",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.icecreamproduction",
                    ),
                ),
                (
                    "moved_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="icecreamproduction",
            name="recipe",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.recipe",
            ),
        ),
    ]
