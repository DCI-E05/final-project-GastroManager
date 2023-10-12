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

class IngredientIncomingAdmin(admin.ModelAdmin):
    # Customize how IngredientIncoming model is displayed in the admin panel
    list_display = ('ingredient', 'quantity', 'unit_weight', 'date_received', 'lot_number', 'expiration_date', 'temperature', 'received_by')
    list_filter = ('ingredient', 'unit_weight')
    search_fields = ('ingredient__name', 'lot_number', 'received_by__username')


class IngredientInventoryAdmin(admin.ModelAdmin):
    # Customize how IngredientInventory model is displayed in the admin panel
    list_display = ('ingredient', 'quantity',)
    list_filter = ('ingredient',)
    search_fields = ('ingredient__name',)


class IceCreamProductionAdmin(admin.ModelAdmin):
    # Customize how IceCreamProduction model is displayed in the admin panel
    list_display = ('recipe', 'container_size', 'quantity_produced', 'date_produced', 'produced_by')
    list_filter = ('recipe__flavor', 'container_size')
    search_fields = ('recipe__flavor', 'produced_by__username')


class IngredientAdmin(admin.ModelAdmin):
    # Customize how Ingredient model is displayed in the admin panel
    list_display = ('name', 'unit_of_measurement')
    search_fields = ('name',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    # Customize how RecipeIngredient model is displayed in the admin panel
    list_display = ('recipe', 'ingredient', 'quantity')
    list_filter = ('recipe__flavor', 'ingredient__name')
    search_fields = ('recipe__flavor', 'ingredient__name')


class StockItemAdmin(admin.ModelAdmin):
    # Customize how StockItem model is displayed in the admin panel
    list_display = ('recipe', 'size', 'quantity', 'date_added', 'added_by')
    list_filter = ('size',)
    search_fields = ('recipe__flavor', 'added_by__username')


class IceCreamStockTakeOutAdmin(admin.ModelAdmin):
    # Customize how IceCreamStockTakeOut model is displayed in the admin panel
    list_display = ('ice_cream_production', 'quantity_moved', 'date_moved', 'moved_by')
    list_filter = ('ice_cream_production__recipe__flavor', 'date_moved')
    search_fields = ('ice_cream_production__recipe__flavor', 'moved_by__username')


# Register models with the custom admin views
admin.site.register(Address)
admin.site.register(StaffMember)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientInventory, IngredientInventoryAdmin)
admin.site.register(IngredientIncoming, IngredientIncomingAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(IceCreamProduction, IceCreamProductionAdmin)
admin.site.register(StockItem, StockItemAdmin)
admin.site.register(IceCreamStockTakeOut, IceCreamStockTakeOutAdmin)
admin.site.register(ManagerUser)
admin.site.register(ServiceUser)
admin.site.register(ProductionUser)