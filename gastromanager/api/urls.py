from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import RecipeListView

urlpatterns = [
    path('blank-login/', TemplateView.as_view(template_name='blank_login.html'), name='blank_login'),
    path("staff/", views.staff_view, name="staff"),
    path("stock/", views.stock_view, name="stock"),
    path("recipes/", RecipeListView.as_view(), name="recipe_list"),
    path("recipes/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("recipes/create/", views.create_recipe, name="create_recipe"),
    path("recipes/update/<int:pk>/", views.update_recipe, name="update_recipe"),
    path("recipes/delete/<int:pk>/", views.delete_recipe, name="delete_recipe"),
    path("stock-takeout/", views.stock_takeout_view, name="stock_takeout"),
    path("add-ingredient/", views.add_ingredient, name="add_ingredient"),
    path("production-calculator/", views.production_calculator_view, name="production_calculator"),
]