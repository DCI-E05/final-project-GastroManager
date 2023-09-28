from django.shortcuts import render
from .models import StockItem, InventoryItem, StaffMember, WorkingHours

def stock_view(request):
    stock = StockItem.objects.first()
    return render(request)

def inventory_view(request):
    inventory = InventoryItem.objects.first()
    return render(request)

def staff_view(request):
    staff = StaffMember.objects.first()
    return render(request)
# Create your views here.
