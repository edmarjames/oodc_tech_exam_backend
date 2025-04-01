from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.price:.2f} - Stock: {self.quantity}"

    def is_in_stock(self):
        return self.quantity > 0

    def reduce_stock(self, amount):
        try:
            if amount > self.quantity:
                raise ValueError("Not enough stock available")

            self.quantity -= amount
            self.save()

            return {"success": True, "message": f"Stock reduced by {amount}. Remaining: {self.quantity}"}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def increase_stock(self, amount):
        try:
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")

            self.quantity += amount
            self.save()

            return {"success": True, "message": f"Stock increased by {amount}. Total: {self.quantity}"}
        except ValueError as e:
            return {"success": False, "error": str(e)}
