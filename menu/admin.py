from django.contrib import admin

# Register your models here.
from .models import Menu, Category



admin.site.register(Menu)
admin.site.register(Category)