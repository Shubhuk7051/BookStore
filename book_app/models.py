from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='customer')
    name=models.CharField(max_length=100, null=True)
    email=models.CharField(max_length=300, null=True)
    
    def __str__(self) -> str:
        return str(self.name)
    
    
class Book(models.Model):
    name=models.CharField(max_length=200, null=True)
    description=models.TextField(default='SOME STRING')
    price=models.DecimalField(default=00000,max_digits=7, decimal_places=2)
    image=models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return str(self.name)
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
 
import uuid   
class Order(models.Model):
    
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='customer')
    book=models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True, related_name='product')
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete_order=models.BooleanField(default=False, null=True, blank=True)
    transaction_id=models.CharField(max_length=200, null=True)
    
    
    @property
    def get_cart_total(self):
        orderitems=self.prod_order_item.all()
        total=sum([item.get_price for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems=self.prod_order_item.all()
        total=sum([item.quantity for item in orderitems])
        return total
    
    @property
    def generate_transaction_id(self):
        if not self.transaction_id:
            # Generate a UUID as the transaction ID
            self.transaction_id = str(uuid.uuid4())
            

class OrderItem(models.Model):
    
    book=models.ForeignKey(Book, on_delete=models.CASCADE,null=True, blank=True,related_name='prod_order')
    order=models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='prod_order_item')
    quantity=models.IntegerField(null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    # Price according to the quantity on cart page
    @property
    def get_price(self):
        if self.book is not None and self.quantity is not None:
            total = self.book.price * self.quantity
            return total
        else:
            return Decimal('0')
    
    
class ShippingAddress(models.Model):
    
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='prod_ship')
    order=models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='ord_ship')
    address=models.CharField(max_length=200, null=True)
    city=models.CharField(max_length=100, null=True)
    state=models.CharField(max_length=100, null=True)
    pincode=models.CharField(max_length=100, null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.address)