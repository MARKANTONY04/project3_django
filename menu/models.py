from django.db import models
from django.utils.text import slugify

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True)
    description = models.TextField(max_length = 300)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    people = models.IntegerField()
    image = models.ImageField(upload_to='menu/')

    # Automatically generate slug from name if slug is not provided
    # Created via copilot and inpired from Mahmood
    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super(Menu, self).save(*args, **kwargs)


    def __str__(self):
        return self.name