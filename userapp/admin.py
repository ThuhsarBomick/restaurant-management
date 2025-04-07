from django.contrib import admin
from userapp.models import Category,Product,Orders,Bill

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Bill)
admin.site.register(Orders)

