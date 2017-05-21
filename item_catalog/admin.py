from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Item, User

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(User)
