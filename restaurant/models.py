from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Booking(models.Model):
    name = models.CharField(max_length=255)
    no_of_guests = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)] , error_messages={'invalid': 'Please enter a number between 1 and 6.'})
    booking_date = models.DateTimeField("", auto_now=False, auto_now_add=False)
    
    def __str__(self):
        return self.name


class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)] , error_messages={'invalid': 'Please enter a number between 1 and 5.'})
    
    def __str__(self):
        return self.title
        