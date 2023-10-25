
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, Recipe, Ingredient, IngredientInventory, IngredientIncoming, RecipeIngredient, IceCreamProduction, StockItem, IceCreamStockTakeOut, Journal 
from .forms import RecipeForm, ProductionCalculatorForm, CustomUserForm, IngredientInventoryUpdateForm, CustomUserNormalForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import F
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from .decorators import manager_required, service_required, production_required, register_activity
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError 
from django.http import Http404
from django.contrib.auth import logout
from django.urls import reverse





# Create a modelformset for RecipeIngredients
RecipeIngredientFormSet = modelformset_factory(RecipeIngredient, fields=('ingredient', 'quantity'), extra=5)

@login_required
def welcome_page(request):
    # Get access level from user
    user_level = request.user.level

    # Dictionary with options depending on acces level.
    options = {
        "Manager": {
            "Edit Profile": "edit_profile",
            "Staff View": "staff_view",
            "Stock View": "stock_view",
            "View Journal": "view_journal",
            "Recipe List": "recipe_list",
            "Production View": "production_view",
            "Stock Takeout View": "stock_takeout_view",
            "Add Ingredient": "add_ingredient",
            "Production Calculator": "production_calculator",
            "Ingredient Inventory": "ingredient_inventory",
        },
        "Service": {
            "Edit Profile": "edit_profile",
            "Stock View": "stock_view",
            "Recipe List": "recipe_list",
            "Stock Takeout View": "stock_takeout_view",
            "Add Ingredient": "add_ingredient",
            "Ingredient Inventory": "ingredient_inventory",

        },
        "Production": {
            "Edit Profile": "edit_profile",
            "Stock View": "stock_view",
            "Recipe List": "recipe_list",
            "Production View": "production_view",
            "Production Calculator": "production_calculator",
            "Add Ingredient": "add_ingredient",
            "Ingredient Inventory": "ingredient_inventory",

        },
} 
  
    # Get specific option according to acces level. This will be used in the main welcome template.
    user_options = options.get(user_level, {})

    return render(request, 'welcome.html', {'user_level': user_level, 'user_options': user_options})


@login_required
@register_activity
def edit_profile(request, user_id=None):
    if user_id is None:
        # If user_id is not provided, edit the profile of the currently logged-in user
        user = request.user
    else:
        # If user_id is provided, edit the profile of the specified user
        user = get_object_or_404(get_user_model(), id=user_id)

    # Check if the current user is an admin or normal user
    is_admin = request.user.userprofile.level == 'Manager'
    is_normal_user = request.user == user

    if request.method == 'POST':
        if is_normal_user:
            form = CustomUserNormalForm(request.POST, instance=user)
        else:
            form = CustomUserForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            if is_admin:
                return redirect('staff')
            else:
                return redirect('edit_profile')

    else:
        form = CustomUserForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form, 'user': user, 'is_admin': is_admin})

login_required
@manager_required
@register_activity
def staff_view(request):
    staff = UserProfile.objects.first()
    user_form = CustomUserForm()  

    if request.method == 'POST':
        if 'add_user' in request.POST:
            user_form = CustomUserForm(request.POST)  
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'User added successfully.')
                return redirect('staff_view')
        elif 'delete_user' in request.POST:
            user_id = request.POST.get('user_id')
            if user_id:
                user = get_object_or_404(get_user_model(), id=user_id)
                user.delete()
                messages.success(request, 'User deleted successfully.')

    users = get_user_model().objects.all()

    return render(request, 'staff_view.html', {'staff': staff, 'user_form': user_form, 'users': users})

@login_required
def stock_view(request):
    stock_items = StockItem.objects.all()
    return render(request, 'stock_view.html', {'stock_items':stock_items})

@login_required
@manager_required
def view_journal(request):
    journal = Journal.objects.all().order_by('-timestamp')
    return render(request, 'journal.html', {'journal': journal})


#had to change auth decorator to use a class based view!
@method_decorator(login_required, name='dispatch')
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe_list.html'
    context_object_name = 'recipes'
#list if recipes
    def get_queryset(self):
        # include ingredients related to that recipe.
        return Recipe.objects.prefetch_related('ingredients')

# View for displaying recipe details
@login_required
@manager_required
@production_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

# This view allows a manager to update an existing recipe.
@login_required
@manager_required
@register_activity
def update_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)

        if form.is_valid():
            recipe = form.save()

            # Check if a new ingredient is being added to the recipe
            new_ingredient_name = form.cleaned_data.get('new_ingredient_name')
            new_ingredient_quantity = form.cleaned_data.get('new_ingredient_quantity')

            if new_ingredient_name and new_ingredient_quantity:
                # Create a new ingredient if it doesn't exist
                new_ingredient, created = Ingredient.objects.get_or_create(
                    name=new_ingredient_name,
                    defaults={'unit_of_measurement': Ingredient.GRAMS}
                )

                # Add the new ingredient to the recipe
                RecipeIngredient.objects.create(
                    recipe=form.instance,
                    ingredient=new_ingredient,
                    quantity=new_ingredient_quantity
                )


            return redirect('recipe_detail', pk=recipe.pk)
    else:
        # Create a form to render the recipe form with the existing data
        form = RecipeForm(instance=recipe)

    return render(request, 'update_recipe.html', {'form': form})



@login_required
@manager_required
@register_activity
def delete_recipe(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')

    return render(request, 'delete_recipe.html', {'recipe': recipe})


@login_required
@manager_required
@register_activity
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)

        if form.is_valid():
            recipe = form.save()

            # Check if a new ingredient is being added to the recipe
            new_ingredient_name = form.cleaned_data.get('new_ingredient_name')
            new_ingredient_quantity = form.cleaned_data.get('new_ingredient_quantity')

            if new_ingredient_name and new_ingredient_quantity:
                # Create a new ingredient if it doesn't exist
                new_ingredient, created = Ingredient.objects.get_or_create(
                    name=new_ingredient_name,
                    defaults={'unit_of_measurement': Ingredient.GRAMS}
                )

                # Add the new ingredient to the recipe
                RecipeIngredient.objects.create(
                    recipe=form.instance,
                    ingredient=new_ingredient,
                    quantity=new_ingredient_quantity
                )


            return redirect('recipe_detail', pk=recipe.pk)
    else:
        # Create a form to render the recipe form
        form = RecipeForm()

    return render(request, 'create_recipe.html', {'form': form})



@login_required
@manager_required
@production_required
@register_activity
def production_view(request):
    if request.method == 'POST':
        recipe_id = request.POST['recipe']
        quantity_produced = request.POST['quantity_produced']
        container_size = request.POST['container_size']  
        produced_by = request.user

        recipe = Recipe.objects.get(pk=recipe_id)
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)

        try:
            # Check ingredient availability in inventory, and catch any ValidationErrors
            check_ingredient_availability(recipe_ingredients, quantity_produced, container_size)

            # Create production
            production = create_production(recipe, container_size, recipe_ingredients, quantity_produced, produced_by)

            # Check if the recipe is marked as a base
            if recipe.is_base:
                # add base to inventory
                add_base_to_inventory(recipe, quantity_produced)
            else:
                # add ice cream to Stock
                update_stock(recipe, production, produced_by)
        except ValidationError as e:
            messages.error(request, e)
            return redirect('production_view')

    return redirect('production_view')

@login_required
@manager_required
@production_required
def check_ingredient_availability(recipe_ingredients, quantity_produced, container_size):
    for recipe_ingredient in recipe_ingredients:
        required_quantity = float(recipe_ingredient.quantity) * quantity_produced * container_size
        inventory = recipe_ingredient.ingredient.inventory

        if inventory.quantity < required_quantity:
            raise ValidationError(f"Ingredient {recipe_ingredient.ingredient.name} is not available in sufficient quantity.")

@login_required
@manager_required
@production_required
@register_activity
def create_production(recipe, container_size, recipe_ingredients, quantity_produced, produced_by):
    # Check if the recipe is marked as a base
    if recipe.is_base:
        # For base recipes, we treat them as a single ingredient
        # Calculate the total quantity required based on quantity produced
        total_quantity_required = quantity_produced

        # Create production
        production = IceCreamProduction.objects.create(
            recipe=recipe,
            quantity_produced=quantity_produced,
            produced_by=produced_by
        )

        # Update inventory for the base (recipe itself)
        base_ingredient, created = Ingredient.objects.get_or_create(
            name=recipe.flavor,
            defaults={'unit_of_measurement': Ingredient.GRAMS}
        )

        base_ingredient.inventory.quantity += total_quantity_required
        base_ingredient.inventory.save()
    else:
        # If it's not a base, then we consider the container size
        # Obtain the quantity factor based on the selected container size
        if container_size == 0.5:
            quantity_factor = 0.5
        elif container_size == 3:
            quantity_factor = 3
        elif container_size == 6:
            quantity_factor = 6
        else:
            raise ValueError("Invalid container size selected")

        # Calculate the total quantity required based on quantity factor and quantity produced
        total_quantity_required = quantity_factor * quantity_produced

        # Create production
        production = IceCreamProduction.objects.create(
            recipe=recipe,
            container_size=container_size,
            quantity_produced=quantity_produced,
            produced_by=produced_by
        )

    # Update ingredient inventory
    for recipe_ingredient in recipe_ingredients:
        required_quantity = float(recipe_ingredient.quantity) * total_quantity_required
        inventory = recipe_ingredient.ingredient.inventory
        inventory.quantity -= required_quantity
        inventory.save()



def add_base_to_inventory(recipe, quantity_produced):
    # Create the base ingredient
    base_ingredient, created = Ingredient.objects.get_or_create(
        name=recipe.flavor,
        defaults={'unit_of_measurement': Ingredient.GRAMS}
    )

    # Update inventory for the base
    base_ingredient.inventory.quantity += float(quantity_produced)
    base_ingredient.inventory.save()

    # Update the inventory for the ingredients used to produce the base
    for ingredient in recipe.base_ingredients.all():
        required_quantity = float(ingredient.recipeingredient_set.get(recipe=recipe).quantity) * float(quantity_produced)
        inventory_entry = IngredientInventory.objects.get(ingredient_name=ingredient)
        inventory_entry.quantity -= required_quantity
        inventory_entry.save()


@receiver(post_save, sender=IceCreamProduction)
def update_stock(sender, instance, created, **kwargs):
    if created:
        # Update ice cream stock
        stock_item, created = StockItem.objects.get_or_create(
            recipe=instance.recipe,
            size=instance.container_size
        )
        stock_item.quantity += instance.quantity_produced
        stock_item.added_by = instance.produced_by
        stock_item.save()

@login_required
@manager_required
@service_required
@register_activity
def stock_takeout_view(request):
    if request.method == 'POST':
        stock_item_id = request.POST['stock_item']
        quantity_moved = request.POST['quantity_moved']
        date_moved = request.POST['date_moved']
        moved_by = request.user

        # Validation: Check if there is enough ice cream in stock
        stock_item = StockItem.objects.get(pk=stock_item_id)

        if float(quantity_moved) <= 0:
            raise ValidationError("Must be positive number")

        if stock_item.quantity < float(quantity_moved):
            raise ValidationError("Not enough in Stock")

        # Register the stock movement
        stock_takeout = IceCreamStockTakeOut.objects.create(
            ice_cream_production=stock_item,
            quantity_moved=quantity_moved,
            date_moved=date_moved,
            moved_by=moved_by
        )

        return redirect('stock_takeout_view')


@login_required
@register_activity
def add_ingredient(request):
    if request.method == 'POST':
        ingredient_name = request.POST['ingredient_name']
        quantity = float(request.POST['quantity'])  # Convert the quantity to a float
        unit_weight = request.POST['unit_weight']
        lot_number = request.POST.get('lot_number', None)
        expiration_date = request.POST.get('expiration_date', None)
        temperature = request.POST.get('temperature', None)
        observations = request.POST.get('observations', None)

        received_by = request.user  # User receiving

        try:
            ingredient = Ingredient.objects.get(name=ingredient_name)
        except Ingredient.DoesNotExist:
            messages.error(request, 'Ingredients doesnt exist')
            return redirect('add_ingredient')

        if quantity <= 0:
            raise ValidationError("quantity must be a positive number.")

        # Call a function to add the ingredient to inventory
        if ingredient.is_base:
            add_base_to_inventory(ingredient, quantity)
        else:
            add_to_inventory(ingredient, quantity)

        # Register the ingredient incoming
        register_ingredient_incoming(ingredient, quantity, lot_number, unit_weight, expiration_date, temperature, observations, received_by)

        messages.success(request, 'Ingredient register succesfully.')
        return redirect('ingredient_inventory')


def add_to_inventory(ingredient, quantity):
    # Get or create the inventory entry
    inventory_entry, created = IngredientInventory.objects.get_or_create(ingredient_name=ingredient)

    # Update the existing quantity with the new quantity if not there than creates it.
    if not created:
        inventory_entry.quantity += quantity
        inventory_entry.save()


def register_ingredient_incoming(ingredient, quantity, lot_number, unit_weight, expiration_date, temperature, observations, received_by):
    # Register for IngredientIncoming
    IngredientIncoming.objects.create(
        ingredient=ingredient,
        quantity=quantity,
        lot_number=lot_number,
        unit_weight=unit_weight,
        expiration_date=expiration_date,
        temperature=temperature,
        observations=observations,
        received_by=received_by
    )

@login_required
def ingredient_inventory_view(request):
    ingredients_inventory = IngredientInventory.objects.all()
    if request.user.userprofile.level == 'Manager': #only manager can make changes.

        if request.method == 'POST':
            #do manual changes en inventory
            form = IngredientInventoryUpdateForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Changes done succesfully.')

    # if there are mistakes in the formulary
    else:
        form = IngredientInventoryUpdateForm()

    return render(request, 'ingredient_inventory.html', {'ingredients_inventory': ingredients_inventory, 'form': form})


@login_required
@manager_required
@production_required
def production_calculator_view(request):
    if request.method == 'POST':
        form = ProductionCalculatorForm(request.POST)
        if form.is_valid():
            recipes = form.cleaned_data['recipes']
            desired_quantities = form.cleaned_data['desired_quantities']
            
            # Parse desired quantities and recipes
            desired_quantities = [float(q.strip()) for q in desired_quantities.split(',')]
            
            # Dictionary to store ingredient quantities
            total_ingredient_quantities = {}
            
            try:
                # Calculate and check availability for each recipe
                for recipe, desired_quantity in zip(recipes, desired_quantities):
                    calculate_production(recipe, desired_quantity, total_ingredient_quantities)
            except ValidationError as e:
                form.add_error(None, e)
            else:
                # Total quantities calculation is successful
                print("Calculations done correctly")
                print(total_ingredient_quantities)

    else:
        form = ProductionCalculatorForm()

    return render(request, 'production_calculator.html', {'form': form})

def calculate_production(recipe, desired_quantity, total_ingredient_quantities):
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    for recipe_ingredient in recipe_ingredients:
        # Get the ingredient and its quantity in the recipe
        ingredient = recipe_ingredient.ingredient
        quantity_in_recipe = float(recipe_ingredient.quantity)  # Quantity per kg

        # Calculate the total quantity needed based on the desired quantity
        total_quantity_needed = quantity_in_recipe * desired_quantity

        # Update or initialize the total_ingredient_quantities dictionary
        if ingredient.id in total_ingredient_quantities:
            total_ingredient_quantities[ingredient.id] += total_quantity_needed
        else:
            total_ingredient_quantities[ingredient.id] = total_quantity_needed

        # Check ingredient availability in inventory
        check_inventory_availability(ingredient, total_quantity_needed)

        # Check if the recipe's base ingredients need to be added
        if recipe.is_base:
            add_base_ingredients(recipe, desired_quantity, total_ingredient_quantities)

# Function to check if base ingredients need to be added
def add_base_ingredients(recipe, desired_quantity, total_ingredient_quantities):
    for base_ingredient in recipe.base_ingredients.all():
        # Get the base ingredient's quantity in the recipe
        recipe_ingredient = base_ingredient.recipeingredient_set.get(recipe=recipe)
        quantity_in_recipe = float(recipe_ingredient.quantity)  # Quantity per kg

        # Calculate the total quantity needed based on the desired quantity
        total_quantity_needed = quantity_in_recipe * desired_quantity

        # Update or initialize the total_ingredient_quantities dictionary for base ingredients
        if base_ingredient.id in total_ingredient_quantities:
            total_ingredient_quantities[base_ingredient.id] += total_quantity_needed
        else:
            total_ingredient_quantities[base_ingredient.id] = total_quantity_needed

        # Check ingredient availability in inventory
        check_inventory_availability(base_ingredient, total_quantity_needed)    

# Function to verify inventory availability
def check_inventory_availability(ingredient, total_quantity_needed):
    inventory = ingredient.inventory

    if inventory.quantity < total_quantity_needed:
        raise ValidationError(f"Ingredient {ingredient.name} is not available in sufficient quantity. Current quantity: {inventory.quantity} kg, Required quantity: {total_quantity_needed} kg")



def custom_logout(request):
    logout(request)
    return redirect("/")