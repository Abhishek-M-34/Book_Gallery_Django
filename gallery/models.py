from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class Book(models.Model):
    seller = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name= 'books'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.title

class Order(models.Model):

    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
    ]

    book = models.ForeignKey(
        Book,
        on_delete= models.CASCADE,
        related_name= "orders"
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name= "orders"
    )
    status = models.CharField(
        max_length= 20,
        choices= STATUS_CHOICES,
        default= 'Pending'
    )
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.buyer.username} - {self.book.title}"