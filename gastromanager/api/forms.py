from django import forms
from .models import Recipe, Ingredient, TimeEntry

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

class ProductionCalculatorForm(forms.Form):
    recipe = forms.ModelChoiceField(
        queryset=Recipe.objects.all(),
        label='Seleccet a recipe'
    )
    
    desired_quantity = forms.DecimalField(
        label='Desire amount (grams or units)',
        widget=forms.TextInput(attrs={'placeholder': 'Enter desire amount'}),
    )

class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['clock_in_time', 'clock_out_time']