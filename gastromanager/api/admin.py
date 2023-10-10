from django.contrib import admin

from .models import (Address, StockItem,StaffMember,IceCreamProduction, IceCreamStockTakeOut, Recipe, Ingredient, IngredientIncoming,IngredientInventory, Base, BaseIngredient, IceCreamBase, RecipeIngredient,ManagerUser,  ServiceUser, ProductionUser )

class IngredientIncomingAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'quantity', 'unit_weight', 'date_received', 'lot_number', 'expiration_date', 'temperature', 'received_by')
    list_filter = ('ingredient', 'unit_weight')
    search_fields = ('ingredient__name', 'lot_number', 'received_by__username')

class IngredientInventoryAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'quantity', 'last_updated')
    list_filter = ('ingredient',)
    search_fields = ('ingredient__name',)

class IceCreamProductionAdmin(admin.ModelAdmin):
    list_display = ('flavor', 'container_size', 'quantity_produced', 'date_produced', 'produced_by')
    list_filter = ('flavor', 'container_size')
    search_fields = ('flavor', 'produced_by__username')

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_of_measurement')
    search_fields = ('name',)


admin.site.register(Address)
admin.site.register(StaffMember)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientInventory, IngredientInventoryAdmin)
admin.site.register(IngredientIncoming, IngredientIncomingAdmin)
admin.site.register(Base)
admin.site.register(BaseIngredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(IceCreamBase)
admin.site.register(IceCreamProduction, IceCreamProductionAdmin)
admin.site.register(StockItem)
admin.site.register(IceCreamStockTakeOut)
admin.site.register(ManagerUser)
admin.site.register(ServiceUser)
admin.site.register(ProductionUser)