from django.db import models
from django.contrib.auth.models import User

CETAGORY_CHOICES = (
    ('LP','Laptop'),
    ('MB','Mobile'),
    ('TB','Tablet'),
    ('LD','Led'),
    ('HP','HeadPhone'),
)

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    sell_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField(default='')
    composition = models.TextField()
    cetagory = models.CharField(choices=CETAGORY_CHOICES,max_length=2)
    product_image=  models.ImageField(upload_to='images')
    
    
    def __str__(self):
        return self.title
    
    
    
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default = 0)
    pincode = models.IntegerField()
    state = models.CharField(max_length = 20)
    
    def __str__(self):
        return self.name


class cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete =models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1 )
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price   
    
    
    
class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    
    def __str__(self):
        return self.name 
    
STATUS_CHOICES =(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    amount = models.IntegerField()
    razorpay_order_id= models.CharField(max_length=100,blank = True,null = True)
    razorpay_payment_status = models.CharField(max_length= 100,blank= True, null=True)
    razorpay_payment_id =models.CharField(max_length= 100,blank= True, null=True)
    paid = models.BooleanField(default = False)
    
    
class orderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    ordered_date = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length = 50,choices = STATUS_CHOICES,default = 'Pending')
    payment = models.ForeignKey(Payment,on_delete = models.CASCADE,null=True, blank=True)
    
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price