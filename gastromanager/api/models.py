from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Address(models.Model):
    line_1 = models.CharField(max_length=255, verbose_name="Address Line 1")
    line_2 = models.CharField(
        max_length=255, verbose_name="Address Line 2", blank=True, null=True
    )
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, verbose_name="Postal Code")
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.line_1}, {self.city}, {self.state}, {self.country}"


class StaffMember(models.Model):
    name = models.CharField(max_length=255)

    date_of_birth = models.DateField()
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE
    )
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    
    LEVEL_CHOICES = [
        ('Service', 'Service'),
        ('Manager', 'Manager'),
        ('Production', 'Production'),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES,default='Service')


    def __str__(self):
        return self.name


# Custom user manager class
class CustomUserManager(BaseUserManager):
    # Create a regular user
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # Create a superuser
    def create_superuser(self, username, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Custom user model for Manager
class ManagerUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    staff_member = models.OneToOneField(
        StaffMember,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='manager_user',
    )
    
    is_staff = models.BooleanField(
        default=True,
        help_text='Designates whether this user can access the admin site.',
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='manager_users', 
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='manager_users_permissions', 
        help_text='Specific permissions for this user.',
        related_query_name='manager_user',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    


# Custom user model for Service
class ServiceUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    staff_member = models.OneToOneField(
        StaffMember,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='service_user',
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='service_users', 
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='service_users_permissions', 
        help_text='Specific permissions for this user.',
        related_query_name='service_user',
    )
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

# Custom user model for Production
class ProductionUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    staff_member = models.OneToOneField(
        StaffMember,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='production_user',
    )
    
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='production_users', 
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='production_users_permissions', 
        help_text='Specific permissions for this user.',
        related_query_name='production_user',
    )
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class WorkingHours(models.Model):
    pass


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    GRAMS = 'grams'
    UNITS = 'units'
    UNIT_CHOICES = [
        (GRAMS, 'Grams'),
        (UNITS, 'Units'),
    ]

    unit_of_measurement = models.CharField(max_length=10, choices=UNIT_CHOICES, default=GRAMS)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

def create_ingredient_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(create_ingredient_slug, sender=Ingredient)

class IngredientInventory(models.Model): #  model tracks the inventory of ingredients.

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        #update inventory before saving
        self.quantity = IngredientIncoming.objects.filter(ingredient=self.ingredient).aggregate(Sum('quantity'))['quantity__sum'] or 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ingredient.name}: {self.quantity} {self.ingredient.unit_of_measurement}"

class IngredientIncoming(models.Model): #  model represents incoming ingredients in the shop.

    GRAMS = 'grams'
    UNITS = 'units'
    UNIT_CHOICES = [
        (GRAMS, 'Grams'),
        (UNITS, 'Units'),
    ]
    
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_weight = models.CharField(max_length=10, choices=UNIT_CHOICES, default=GRAMS)
    date_received = models.DateTimeField(auto_now_add=True)  #date time automatic
    lot_number = models.CharField(max_length=255, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    received_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update Inventory
        inventory, created = IngredientInventory.objects.get_or_create(ingredient=self.ingredient)
        inventory.quantity += float(self.quantity)
        inventory.save()

    def __str__(self):
        return f"{self.ingredient.name}: {self.quantity} received on {self.date_received}"



class StockItem(models.Model): # model represents IceCream in stock.

    flavor = models.CharField(max_length=255, default="")
    size = models.FloatField(choices=[(0.5, '0.5 Litres'), (3, '3 Litres'), (6, '6 Litres')],default=0.5)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.flavor} ({self.size}L) - {self.quantity} in stock"


    
class Base(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ingredients = models.ManyToManyField(Ingredient, through='BaseIngredient')

    def __str__(self):
        return self.name    
    
class Recipe(models.Model):
    flavor = models.CharField(max_length=255, unique=True)
    base = models.ManyToManyField(Base, through='RecipeBase', related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='recipes')
    quantity_per_kilo = models.DecimalField(max_digits=10, decimal_places=2, default=1000)

    def __str__(self):
        return self.flavor    

class IceCreamProduction(models.Model):
    flavor = models.CharField(max_length=255)
    container_size = models.FloatField(choices=[(0.5, '0.5 Litres'), (3, '3 Litres'), (6, '6 Litres')])
    quantity_produced = models.DecimalField(max_digits=10, decimal_places=2)
    date_produced = models.DateTimeField(auto_now_add=True)
    produced_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe, related_name='productions')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update inventary 
        for recipe in self.recipes.all():
            for recipe_ingredient in recipe.ingredients.all():
                inventory, created = IngredientInventory.objects.get_or_create(ingredient=recipe_ingredient.ingredient)
                inventory.quantity -= (recipe_ingredient.quantity * self.quantity_produced)
                inventory.save()

    def __str__(self):
        return f"{self.flavor} ({self.container_size}L) - {self.quantity_produced} produced on {self.date_produced}"
    
class IceCreamStockTakeOut(models.Model): # model represents ice cream takn out of stock.

    ice_cream_production = models.ForeignKey(IceCreamProduction, on_delete=models.CASCADE)
    quantity_moved = models.DecimalField(max_digits=10, decimal_places=2)
    date_moved = models.DateTimeField()
    moved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ice_cream_production.flavor} ({self.ice_cream_production.container_size}L) - {self.quantity_moved} sold on {self.date_moved}"

class BaseIngredient(models.Model):
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.base.name} - {self.ingredient.name}: {self.quantity}"
    

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.recipe} - {self.ingredient.name}: {self.quantity}"


    
class IceCreamBase(models.Model): # model represents the relationship between an ice cream recipe and a base.

    ice_cream = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    base = models.ForeignKey(Base, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.ice_cream.flavor} - {self.base.name}"
    
class RecipeBase(models.Model): # model represents the quantity of a base in a recipe.

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.recipe} - {self.base.name}: {self.quantity}"
    

