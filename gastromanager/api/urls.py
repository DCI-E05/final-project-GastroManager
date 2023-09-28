from django.urls import path
from .views import staff_view, inventory_view, stock_view

urlpatterns = [
    path("stock", stock_view, name="stock"),
    path("staff", staff_view, name ="staff"),
    path("inventory", inventory_view, name ="inventory")
]