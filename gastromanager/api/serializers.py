from rest_framework import serializers
from .models import StaffMember, StockItemName, StockItem, InventoryItem, WorkingHours


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"


class StockItemNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItemName
        fields = "__all__"


class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = "__all__"


class StaffMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = "__all__"
