from django.db import models

class InventoryItem(models.Model):
    item_no = models.CharField(max_length=50, unique=True)
    item_type = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_date = models.DateTimeField()

    # Meta subclass to ensure correct human-readable naming in the Admin panel
    class Meta:
        verbose_name_plural = "Inventory Items"

    # Human-readable label representation string
    def __str__(self):
        return f"{self.item_no} - {self.name}"