from django.db import models

class Address(models.Model):
    line_1 = models.CharField(max_length=255, verbose_name="Address Line 1")
    line_2 = models.CharField(max_length=255, verbose_name="Address Line 2", blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, verbose_name="Postal Code")
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.line_1}, {self.city}, {self.state}, {self.country}"

class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    batch_number = models.CharField(max_length=20, blank=True)
    production_date = models.DateField(blank=True)
    expiration_date = models.DateField(blank=True)
    temperature = models.IntegerField(blank=True)
    #employee = models.ForeignKey(on_delete=models.CASCADE)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class StockItem(models.Model):
    SIZE_CHOICES = [
        (0.5, '0.5 Litres'),
        (3, '3 Litres '),
        (6, '6 Litres ')
    ]
    name = models.CharField(max_length=255)
    size = models.FloatField(choices=SIZE_CHOICES)
    quantity = models.IntegerField()
    production_date = models.DateField()
    expiration_date = models.DateField()
    #employee = models.ForeignKey(on_delete=models.CASCADE)
    comment = models.TextField(blank=True)

    

class StaffMember(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)## problem for the future
    email = models.CharField(max_length=255)
    phone = models.CharField()

class WorkingHours(models.Model):
    pass