
from django.shortcuts import render, redirect,get_list_or_404, get_object_or_404
from .models import StockItem, StaffMember, StaffMember, Recipe, Ingredient, IngredientInventory, IngredientIncoming, IceCreamProduction, StockItem, IceCreamStockTakeOut
from .forms import RecipeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required




def staff_view(request):
    staff = StaffMember.objects.first()
    return render(request)

def stock_view(request):
    stock = StockItem.objects.first()
    return render(request)


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'create_recipe.html', {'form': form})

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

def ice_cream_production_view(request):
    ice_cream_production = IceCreamProduction.objects.first()
    return render(request)

def stock_item_view(request):
    stock_item = StockItem.objects.first()
    return render(request)

def ice_cream_stock_takeout_view(request):
    ice_cream_stock_takeout = IceCreamStockTakeOut.objects.first()
    return render(request)


@login_required
def add_ingredient(request):
    if request.method == 'POST':
        ingredient_name = request.POST['ingredient_name']
        quantity = request.POST['quantity']
        unit_weight = request.POST['unit_weight']
        lot_number = request.POST.get('lot_number', None)
        expiration_date = request.POST.get('expiration_date', None)
        temperature = request.POST.get('temperature', None)
        observations = request.POST.get('observations', None)
        
        received_by = request.user  # User 
        
        try:
            ingredient = Ingredient.objects.get(name=ingredient_name)
        except Ingredient.DoesNotExist:
            messages.error(request, 'Ingredient doesnt existe.')
            return redirect('add_ingredient')
        
        # register for IngredientIncoming
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
        
        # Update Inventory
        inventory, created = IngredientInventory.objects.get_or_create(ingredient=ingredient)
        inventory.quantity += float(quantity)
        inventory.save()
        
        messages.success(request, 'Ingredient succesfully registered.')
        return redirect('ingredient_inventory')
    
    # List of available ingrdnts
    ingredients = Ingredient.objects.all()
    return render(request, 'add_ingredient.html', {'ingredients': ingredients})

class staff_view(generics.ListCreateAPIView):
    queryset = StaffMember.objects.all()
    serializer_class = StaffMemberSerializer
