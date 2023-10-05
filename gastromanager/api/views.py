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
