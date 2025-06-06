from django.db import models

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length = 300)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    people = models.IntegerField()
    image = models.ImageField(upload_to='menu/')


def __str__(self):
    return self.name