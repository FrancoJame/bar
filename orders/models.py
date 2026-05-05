from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    staff_member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='recorded_orders')
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=[('CASH', 'Cash'), ('MOBILE_MONEY', 'Mobile Money')], default='CASH')
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_phone = models.CharField(max_length=20, blank=True, null=True)
    staff_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Staff Name")

    @property
    def change(self):
        return max(self.amount_paid - self.total_amount, 0)

    def __str__(self):
        return f"Order #{self.id} by {self.staff_member.username if self.staff_member else 'Unknown'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
