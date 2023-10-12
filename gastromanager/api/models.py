from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission


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
    
    # Choices for the staff member's role
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


class Ingredient(models.Model): # Model to represent an ingredient

    name = models.CharField(max_length=255, unique=True)

    GRAMS = 'grams'
    UNITS = 'units'
    UNIT_CHOICES = [
        (GRAMS, 'Grams'),
        (UNITS, 'Units'),
    ]

    unit_of_measurement = models.CharField(max_length=10, choices=UNIT_CHOICES, default=GRAMS)

    def __str__(self):
        return self.name
    

    def get_inventory(self):
        # return the inventory of the related ingredient.
        return IngredientInventory.objects.filter(ingredient_name=self)


class IngredientInventory(models.Model):
    ingredient_name = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True)  # Changed to DecimalField to handle decimals

    def __str__(self):
        unit = self.ingredient_name.unit_of_measurement  # Get the unit of measurement from the related Ingredient
        if unit == "grams":
            # If the unit is "grams," display the quantity in grams
            return f"{self.ingredient_name.name}: {self.quantity} {unit}"
        elif unit == "units":
            # If the unit is "units," display the quantity in units
            return f"{self.ingredient_name.name}: {int(self.quantity)} {unit}"
        else:
            # If the unit is neither "grams" nor "units," display only the ingredient name
            return self.ingredient_name.name
        
    @classmethod
    def update_or_create_inventory(cls, ingredient, new_quantity):
        # Get the existing inventory entry for the given ingredient
        inventory_entry, created = cls.objects.get_or_create(ingredient=ingredient)

        # If a new entry was created, set the quantity to the new quantity
        if created:
            inventory_entry.quantity = new_quantity
        else:
            # If the entry already existed, simply add the new quantity to the existing quantity
            inventory_entry.quantity += new_quantity

        inventory_entry.save()

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
    received_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False, null=True, blank=True)


    def __str__(self):
        return f"{self.ingredient.name}: {self.quantity} received on {self.date_received}"


class Recipe(models.Model):
    flavor = models.CharField(max_length=255, unique=True)
    is_base = models.BooleanField(default=False)  # to identify as base or ice cream
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient')

    def __str__(self):
        return self.flavor
    
class RecipeIngredient(models.Model): # Model to represent the ingredients in a recipe
    recipe_name = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.recipe_name} - {self.ingredient.name}: {self.quantity}"
    
class StockItem(models.Model): # model represents IceCream in stock.

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, default=None)
    size = models.FloatField(choices=[(0.5, '0.5 Litres'), (3, '3 Litres'), (6, '6 Litres')], default=0.5)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe} ({self.size}L) - {self.quantity} in stock"


class IceCreamProduction(models.Model): # Model to represent ice cream production
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, default=None)
    container_size = models.FloatField(choices=[(0.5, '0.5 Litres'), (3, '3 Litres'), (6, '6 Litres')])
    quantity_produced = models.DecimalField(max_digits=10, decimal_places=2)
    date_produced = models.DateTimeField(auto_now_add=True)
    produced_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe} ({self.container_size}L) - {self.quantity_produced} produced on {self.date_produced}"
    
class IceCreamStockTakeOut(models.Model): # model represents ice cream takn out of stock.

    ice_cream_production = models.ForeignKey(IceCreamProduction, on_delete=models.CASCADE)
    quantity_moved = models.DecimalField(max_digits=10, decimal_places=2)
    date_moved = models.DateTimeField()
    moved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ice_cream_production.recipe} ({self.ice_cream_production.container_size}L) - {self.quantity_moved} sold on {self.date_moved}"




