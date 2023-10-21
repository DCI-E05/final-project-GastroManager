
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile,Recipe, Ingredient, IngredientInventory, IngredientIncoming, RecipeIngredient, IceCreamProduction, StockItem, IceCreamStockTakeOut 
from .forms import RecipeForm, ProductionCalculatorForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import F
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from .decorators import manager_required, service_required, production_required
from django.utils.decorators import method_decorator




RecipeIngredientFormSet = modelformset_factory(RecipeIngredient, fields=('ingredient', 'quantity'), extra=5)


@login_required
def staff_view(request):
    staff = UserProfile.objects.first()
    return render(request, 'staff_view.html', {'staff': staff})

@login_required
def stock_view(request):
    stock_items = StockItem.objects.all()
    return render(request, 'stock_view.html', {'stock_item':stock_items})

#had to change auth decorator to use it class based view!
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

@login_required
@manager_required
def create_recipe(request):
    if request.method == 'POST':
        # Create a RecipeForm instance from the POST data
        form = RecipeForm(request.POST)
        # Create a RecipeIngredientFormSet instance from the POST data
        formset = RecipeIngredientFormSet(request.POST, queryset=RecipeIngredient.objects.none())

        if form.is_valid() and formset.is_valid():
            # Save the recipe
            recipe = form.save()

            # Associate the recipe with ingredients and quantities
            instances = formset.save(commit=False)
            for instance in instances:
                instance.recipe = recipe
                instance.save()

            return redirect('recipe_detail', pk=recipe.pk)
    else:
        # Create a RecipeForm instance for rendering the recipe form
        form = RecipeForm()
        # Create a RecipeIngredientFormSet instance for rendering the ingredient formset
        formset = RecipeIngredientFormSet(queryset=RecipeIngredient.objects.none())

    # Render the recipe form and the ingredient formset
    return render(request, 'create_recipe.html', {'form': form, 'formset': formset})

@login_required
@manager_required
def update_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'update_recipe.html', {'form': form})

@login_required
@manager_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'delete_recipe.html', {'recipe': recipe})


@login_required
@manager_required
@production_required
def production_view(request):
    if request.method == 'POST':
        recipe_id = request.POST['recipe']
        quantity_produced = request.POST['quantity_produced']
        produced_by = request.user

        recipe = Recipe.objects.get(pk=recipe_id)
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)

        # Check ingredient availability in inventory
        check_ingredient_availability(recipe_ingredients, quantity_produced)

        # Create production
        production = create_production(recipe, recipe_ingredients, quantity_produced, produced_by)

        # Check if the recipe is marked as a base
        if recipe.is_base:
            # add base to inventary
            add_base_to_inventory(recipe, quantity_produced)
        else:
            # add ice cream to Stock
            update_stock(recipe, production, produced_by)

        return redirect('production_view')

@login_required
@manager_required
@production_required
def check_ingredient_availability(recipe_ingredients, quantity_produced):
    for recipe_ingredient in recipe_ingredients:
        required_quantity = float(recipe_ingredient.quantity) * float(quantity_produced)
        inventory = recipe_ingredient.ingredient.inventory

        if inventory.quantity < required_quantity:
            raise ValidationError(f"Ingredient {recipe_ingredient.ingredient.name} is not available in sufficient quantity.")

@login_required
@manager_required
@production_required
def create_production(recipe, recipe_ingredients, quantity_produced, produced_by):
    # Create production
    production = IceCreamProduction.objects.create(
        recipe=recipe,
        quantity_produced=quantity_produced,
        produced_by=produced_by
    )

    # Update ingredient inventory
    for recipe_ingredient in recipe_ingredients:
        required_quantity = float(recipe_ingredient.quantity) * float(quantity_produced)
        inventory = recipe_ingredient.ingredient.inventory
        inventory.quantity -= required_quantity
        inventory.save()
    # Check if the recipe is marked as a base
    if recipe.is_base:
        add_base_to_inventory(recipe, quantity_produced)

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


def update_stock(recipe, production, produced_by):
    # Update ice cream stock
    stock_item, created = StockItem.objects.get_or_create(
        recipe=recipe,
        size=production.container_size
    )
    stock_item.quantity += production.quantity_produced
    stock_item.added_by = produced_by
    stock_item.save()



@receiver(post_save, sender=IceCreamProduction)
def update_stock_on_production(sender, instance, created, **kwargs):
    if created:
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
def stock_takeout_view(request):
    if request.method == 'POST':
        stock_item_id = request.POST['stock_item']
        quantity_moved = request.POST['quantity_moved']
        date_moved = request.POST['date_moved']
        moved_by = request.user

        # Validation: Check if there is enough ice cream in stock
        stock_item = StockItem.objects.get(pk=stock_item_id)

        if float(quantity_moved) <= 0:
            raise ValidationError("La cantidad debe ser un número positivo.")

        if stock_item.quantity < float(quantity_moved):
            raise ValidationError("No hay suficiente helado en stock.")

        # Register the stock movement
        stock_takeout = IceCreamStockTakeOut.objects.create(
            ice_cream_production=stock_item,
            quantity_moved=quantity_moved,
            date_moved=date_moved,
            moved_by=moved_by
        )

        return redirect('take_out_ice_cream')


@login_required
@manager_required
@service_required
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
@manager_required
@production_required
def production_calculator_view(request):
    if request.method == 'POST':
        form = ProductionCalculatorForm(request.POST)
        if form.is_valid():
            recipe = form.cleaned_data['recipe']
            desired_quantity = form.cleaned_data['desired_quantity']
            
            # Make calculations and check availability
            try:
                with transaction.atomic():
                    calculate_production(recipe, desired_quantity)
            except ValidationError as e:
                form.add_error(None, e)
            else:
                print("Calculations done correctly")

    else:
        form = ProductionCalculatorForm()

    return render(request, 'production_calculator.html', {'form': form})

# function to calculate depending on inventary
def calculate_production(recipe, desired_quantity):
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    check_ingredient_availability(recipe_ingredients, desired_quantity)

