from django.db import models

# Create your models here.
class proreg(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    email=models.EmailField(max_length=100)
    category=models.CharField(max_length=100)
    upload_doc = models.FileField(upload_to="professional_docs/",
                                  blank=True,
                                  null=True)
    id_proof = models.FileField(upload_to="id_proofs/")

    password = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )

    profile_pic = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True
    )

    address = models.TextField()
    
    service_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    location = models.CharField(
        max_length=255,
        blank=True
    )

    experience = models.PositiveIntegerField(
        null=True,
        blank=True
    )



    def __str__(self):
            return f"{self.name}"