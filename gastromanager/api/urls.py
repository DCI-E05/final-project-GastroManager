from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('blank-login/', TemplateView.as_view(template_name='blank_login.html'), name='blank_login'),
    path("staff/", views.staff_view, name="staff"),
    path("stock/", views.stock_view, name="stock"),
    path("recipes/", views.RecipeListView.as_view(), name="recipe_list"),
    path("recipes/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("recipes/create/", views.create_recipe, name="create_recipe"),
    path("recipes/update/<int:pk>/", views.update_recipe, name="update_recipe"),
    path("recipes/delete/<int:pk>/", views.delete_recipe, name="delete_recipe"),
    path("ingredients/", views.ingredient, name="ingredient"),
    path("ingredient-inventory/", views.ingredient_inventory_view, name="ingredient_inventory"),
    path("ingredient-incoming/", views.ingredient_incoming_view, name="ingredient_incoming"),
    path("production/", views.production_view, name="production"),
    path("stock-item/", views.stock_item_view, name="stock_item"),
    path("stock-takeout/", views.stock_takeout_view, name="stock_takeout"),
    path("add-ingredient/", views.add_ingredient, name="add_ingredient"),
    path('stock/', views.stock_view, name='stock_view'),
]