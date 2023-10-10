from django.urls import path
from . import views

urlpatterns = [
    path("staff/", views.staff_view, name="staff"),
    path("stock/", views.stock_view, name="stock"),
    path("recipes/", views.recipe_list, name="recipe_list"),
    path("recipe/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("recipe/create/", views.create_recipe, name="create_recipe"),
    path("recipe/update/<int:pk>/", views.update_recipe, name="update_recipe"),
    path("recipe/delete/<int:pk>/", views.delete_recipe, name="delete_recipe"),
    path("ingredients/", views.ingredient, name="ingredient"),
    path("ingredient-inventory/", views.ingredient_inventory_view, name="ingredient_inventory"),
    path("ingredient-incoming/", views.ingredient_incoming_view, name="ingredient_incoming"),
    path("ice-cream-production/", views.ice_cream_production_view, name="ice_cream_production"),
    path("stock-item/", views.stock_item_view, name="stock_item"),
    path("ice-cream-stock-takeout/", views.ice_cream_stock_takeout_view, name="ice_cream_takeout"),
    path("add-ingredient/", views.add_ingredient, name="add_ingredient"),
]