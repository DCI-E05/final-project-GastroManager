from django.contrib import admin

from .models import (Address, StockItem, StaffMember, IceCreamProduction, IceCreamStockTakeOut, Recipe, Ingredient, IngredientIncoming, IngredientInventory, RecipeIngredient, ManagerUser, ServiceUser, ProductionUser)

# Define an inline model for RecipeIngredient
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 5  # Adjust this number to control how many ingredients you can add at once

# Customize the Recipe model in the admin panel
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('flavor', 'is_base')
    list_filter = ('is_base',)
    search_fields = ('flavor',)
    inlines = [RecipeIngredientInline]  # Add the inline model to the Recipe admin

# Register models with the custom admin views
admin.site.register(Address)
admin.site.register(StaffMember)
admin.site.register(Ingredient)
admin.site.register(IngredientInventory)
admin.site.register(IngredientIncoming)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(IceCreamProduction)
admin.site.register(StockItem)
admin.site.register(IceCreamStockTakeOut)
admin.site.register(ManagerUser)
admin.site.register(ServiceUser)
admin.site.register(ProductionUser)