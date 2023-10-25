from django import forms
from .models import Recipe, Ingredient, UserProfile, IngredientInventory
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError




class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['flavor', 'ingredients', 'base_ingredients']

    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    base_ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Ajusta esto según tus necesidades
    )

    ingredient_quantities = forms.DecimalField(
        label='Ingredient Quantities (grams or units)',
        widget=forms.TextInput(attrs={'placeholder': 'Enter quantities for selected ingredients'}),
        required=False,
    )

    new_ingredient_name = forms.CharField(
        max_length=255,
        label='New Ingredient Name',
        required=False,
    )
    
    new_ingredient_quantity = forms.DecimalField(
        label='New Ingredient Quantity',
        required=False,
    )

class ProductionCalculatorForm(forms.Form):
    recipes = forms.ModelMultipleChoiceField(
        queryset=Recipe.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Recipes for Production"
    )
    desired_quantities = forms.CharField(
        label='Desired Quantities (kg)', 
        help_text='Enter the desired quantities for the selected recipes, separated by commas'
    )
    

class CustomUserForm(UserChangeForm): #for manager
    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'date_of_birth', 'address', 'phone', 'level', 'is_active', 'is_staff', 'is_superuser')

class CustomUserNormalForm(forms.ModelForm): #for all users
    class Meta:
        model = UserProfile
        fields = ('password', 'first_name', 'last_name', 'email', 'date_of_birth', 'address', 'phone',)

# Ingredient Inventory Update Form
class IngredientInventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = IngredientInventory
        fields = ('quantity',)

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise ValidationError("Quantity must be a positive number.")
        return quantity
