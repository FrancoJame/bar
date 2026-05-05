from django.db import models
from django.conf import settings

class LoungeRoom(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    description = models.TextField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    price_full_day = models.DecimalField(max_digits=10, decimal_places=2, default=30000.00)
    image = models.ImageField(upload_to='lounges/', blank=True, null=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('AVAILABLE', 'Room available'),
        ('BUSY', 'Room busy'),
        ('FREE_SOON', 'The Room is free in the next Hour'),
        ('UNAVAILABLE', 'Room not available'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    room = models.ForeignKey(LoungeRoom, on_delete=models.CASCADE, related_name='bookings')
    booking_type = models.CharField(max_length=20, choices=[('HOURLY', 'Hourly'), ('FULL_DAY', 'Full Day')], default='HOURLY')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Customer Info
    customer_nin = models.CharField(max_length=50, blank=True, null=True, verbose_name="Name or NIN")
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.user.username} - {self.room.name}"
