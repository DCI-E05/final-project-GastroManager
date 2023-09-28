# from django.shortcuts import render
# from .models import StockItem, InventoryItem, StaffMember, WorkingHours


# def stock_view(request):
#     stock = StockItem.objects.first()
#     return render(request)


# def inventory_view(request):
#     inventory = InventoryItem.objects.first()
#     return render(request)


# def staff_view(request):
#     staff = StaffMember.objects.first()
#     return render(request)


# # Create your views here.

from rest_framework import generics
from .models import InventoryItem, StockItem, StaffMember, StockItemName
from .serializers import (
    InventoryItemSerializer,
    StockItemSerializer,
    StaffMemberSerializer,
    StockItemNameSerializer,
)


class inventory_view(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer


class stock_name_view(generics.ListCreateAPIView):
    queryset = StockItemName.objects.all()
    serializer_class = StockItemNameSerializer


class stock_view(generics.ListCreateAPIView):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer


class staff_view(generics.ListCreateAPIView):
    queryset = StaffMember.objects.all()
    serializer_class = StaffMemberSerializer
