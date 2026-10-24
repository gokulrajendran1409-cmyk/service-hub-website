from django.db import models

# Create your models here.
class userreg(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=200)
    phone=models.CharField(max_length=15, null=True)
    password=models.CharField(max_length=200,null=True)

    def __str__(self):
        return f"{self.name}"

class category(models.Model):
    name=models.CharField(max_length=200)
    desc=models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"


from django.conf import settings
from django.db import models


class Booking(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(
    'user.userreg',
    on_delete=models.CASCADE,
    related_name='service_bookings'
)

    professional = models.ForeignKey(
        'professional.proreg',
        on_delete=models.PROTECT,
        related_name='bookings'
    )

    service_description = models.TextField()

    service_address = models.TextField()

    contact_number = models.CharField(max_length=15)

    booking_date = models.DateField()

    booking_time = models.TimeField()

    service_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.pk} - {self.status}"
    