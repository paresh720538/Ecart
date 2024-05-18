from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Product)
admin.site.register(models.Customer)
admin.site.register(models.cart)
admin.site.register(models.Payment)
admin.site.register(models.orderPlaced)