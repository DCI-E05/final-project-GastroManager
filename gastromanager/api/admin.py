from django.contrib import admin
from .models import InventoryItem, Address, StockItem, StaffMember

admin.site.register(InventoryItem)
admin.site.register(StaffMember)
admin.site.register(Address)
admin.site.register(StockItem)


# Register your models here.
