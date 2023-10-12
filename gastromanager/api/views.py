
from django.shortcuts import render, redirect, get_object_or_404
from .models import StockItem, StaffMember, StaffMember, Recipe, Ingredient, IngredientInventory, IngredientIncoming, RecipeIngredient, IceCreamProduction, StockItem, IceCreamStockTakeOut 
from .forms import RecipeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import F
from django.forms import modelformset_factory

RecipeIngredientFormSet = modelformset_factory(RecipeIngredient, fields=('ingredient', 'quantity'), extra=5)



def staff_view(request):
    staff = StaffMember.objects.first()
    return render(request)

def stock_view(request):
    stock_items = StockItem.objects.all()
    return render(request, 'stock_view.html', {'stock_item':stock_items})

# List view for recipes
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        # include ingredients related to that recipe.
        return Recipe.objects.prefetch_related('ingredients')

# View for displaying recipe details
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

@login_required
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

def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'delete_recipe.html', {'recipe': recipe})


def ingredient(request):
    ingredient = Ingredient.objects.first()
    return render(request)


def ingredient_inventory_view(request):
    ingredient_inventory = IngredientInventory.objects.all()
    return render(request)


def ingredient_incoming_view(request):
    ingredient_incoming = IngredientIncoming.objects.first()
    return render(request)

@login_required
def production_view(request):
    if request.method == 'POST':
        recipe_id = request.POST['recipe']
        quantity_produced = request.POST['quantity_produced']
        produced_by = request.user

        #Validation:
        #First obtain recipe and ingredients:
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)

        #check availability in Inventory:
        for recipe_ingredient in recipe_ingredients:
            inventory = IngredientInventory.objects.get(ingredient=recipe_ingredient.ingredient)
            if inventory.quantity < float(recipe_ingredient.quantity) * float(quantity_produced):
                messages.error(request, f"Ingredient {recipe_ingredient.ingredient.name} is not available in sufficient quantity.")
                return redirect('production_view')

        # Create producción
        production = IceCreamProduction.objects.create(recipe_id=recipe_id, quantity_produced=quantity_produced, produced_by=produced_by)

        # Update ingredient inventory
        recipe = Recipe.objects.get(pk=recipe_id)
        for ingredient in recipe.ingredients.all():
            inventory, created = IngredientInventory.objects.get_or_create(ingredient=ingredient)
            inventory.quantity -= (float(RecipeIngredient.objects.get(recipe=recipe, ingredient=ingredient).quantity) * float(quantity_produced))
            inventory.save()

        # If this production is of a base, also update the inventory
        if recipe.is_base:
            base_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
            for base_ingredient in base_ingredients:
                inventory, created = IngredientInventory.objects.get_or_create(ingredient=base_ingredient.ingredient)
                inventory.quantity -= (float(base_ingredient.quantity) * float(quantity_produced))
                inventory.save()

        # Uodate Icecream Stock
        stock_item, created = StockItem.objects.get_or_create(recipe=recipe, size=production.container_size)
        stock_item.quantity += production.quantity_produced
        stock_item.added_by = produced_by
        stock_item.save()

        return redirect('production_view')

def stock_item_view(request):
    stock_item = StockItem.objects.first()
    return render(request)

@login_required
def stock_takeout_view(request):
    if request.method == 'POST':
        stock_item_id = request.POST['stock_item']
        quantity_moved = request.POST['quantity_moved']
        date_moved = request.POST['date_moved']
        moved_by = request.user

        # Register stock movement
        stock_item = StockItem.objects.get(pk=stock_item_id)
        stock_takeout = IceCreamStockTakeOut.objects.create(stock_item=stock_item, quantity_moved=quantity_moved, date_moved=date_moved, moved_by=moved_by)

        # Update the quantity in stock
        stock_item.quantity = F('quantity') - float(quantity_moved)
        stock_item.save()

        return redirect('stock_takeout_view')


@login_required
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
            messages.error(request, 'The ingredient does not exist.')
            return redirect('add_ingredient')

        # Get or create the inventory entry
        inventory_entry, created = IngredientInventory.objects.get_or_create(ingredient=ingredient)

        # Update the existing quantity with the new quantity
        inventory_entry.quantity += quantity
        inventory_entry.save()

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

        messages.success(request, 'Ingredient registered successfully.')
        return redirect('ingredient_inventory')
