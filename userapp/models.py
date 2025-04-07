from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    Category_name=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    def __str__(self):
        return self.Category_name
    
class Product(models.Model):
    product_name=models.CharField(max_length=100)
    price=models.FloatField()
    Category=models.ForeignKey(Category,on_delete=models.CASCADE)  
    description=models.TextField()
    image=models.ImageField(upload_to='media/')
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.product_name
    

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    options=(
        ('in-cart','in-cart'),
        ('order-placed','order-placed'),
        ('cancelled','cancelled'),

     )
    status=models.CharField(max_length=100,choices=options,default='in-cart')
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
    
class Orders(models.Model):
    product=models.ForeignKey(Cart,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    table_No=models.TextField(max_length=200)
    options=(
        ('order-placed','order-placed'),
        ('cancelled','cancelled'),
        ('preparing','preparing'),
        ('Order-Prepared','Order-Prepared'),
     )
    status=models.CharField(max_length=100,choices=options,default='order-placed')
    quantity = models.IntegerField(default=1) 
    price = models.FloatField() 
    date=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)   

class Bill(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total=models.FloatField()
    table_No=models.TextField(max_length=200)
    date=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username