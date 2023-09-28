from django.urls import path
from .views import staff_view, inventory_view, stock_view, stock_name_view

urlpatterns = [
    path("stock", stock_view.as_view(), name="stock"),
    path("staff", staff_view.as_view(), name="staff"),
    path("inventory", inventory_view.as_view(), name="inventory"),
    path("stockname", stock_name_view.as_view(), name="stockname"),
]
