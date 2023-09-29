from django.contrib import admin
from .models import (
    InventoryItem,
    Address,
    StockItem,
    StaffMember,
    StockItemName,
    StockItem,
)

admin.site.register(InventoryItem)
admin.site.register(StaffMember)
admin.site.register(Address)
admin.site.register(StockItem)
admin.site.register(StockItemName)


# Register your models here.
