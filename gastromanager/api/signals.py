from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import IngredientIncoming, IngredientInventory, IceCreamProduction, StockItem

@receiver(post_save, sender=IngredientIncoming)
def update_inventory(sender, instance, created, **kwargs):
    if created:
        # Update or create the inventory entry for the received ingredient
        inventory, _ = IngredientInventory.objects.get_or_create(ingredient=instance.ingredient)
        if inventory.quantity is None:
            inventory.quantity = instance.quantity
        else:
            inventory.quantity += instance.quantity
        inventory.save()

@receiver(post_save, sender=IceCreamProduction)
def update_stock_on_production(sender, instance, created, **kwargs):
    if created:
        stock_item, created = StockItem.objects.get_or_create(recipe=instance.recipe, size=instance.container_size)
        stock_item.quantity += instance.quantity_produced
        stock_item.added_by = instance.produced_by
        stock_item.save()