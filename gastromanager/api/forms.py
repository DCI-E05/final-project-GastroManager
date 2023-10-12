from django import forms
from .models import Recipe, Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['flavor', 'is_base']  # Fields to be included in the form

    # Multiple choice field for ingredients using checkboxes
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),  # Queryset to populate the choices
        widget=forms.CheckboxSelectMultiple,  # Checkbox widget for ingredient selection
    )

    # Decimal field for ingredient quantities with optional input
    ingredient_quantities = forms.DecimalField(
        label='Ingredient Quantities (grams or units)',  # Label for the field
        widget=forms.TextInput(attrs={'placeholder': 'Enter quantities for selected ingredients'}),  # Placeholder text for input
        required=False,  # Field is not required (optional)
    )