from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import IngredientIncoming, IngredientInventory

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