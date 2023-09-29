from django.urls import path
from .views import staff_view, inventory_view, stock_view, stock_name_view

urlpatterns = [
    path("stock/", stock_view.as_view(), name="stock_view"),
    path("staff/", staff_view.as_view(), name="staff_view"),
    path("inventory/", inventory_view.as_view(), name="inventory_view"),
    path("stock_name/", stock_name_view.as_view(), name="stock_name_view"),
]
