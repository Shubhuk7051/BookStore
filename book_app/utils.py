from .models import Customer
from django.contrib.auth.models import User
from .models import *

def get_or_create_customer(user):
    try:
        customer = user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=user)
    return customer

def orderData(request):
    
    user = request.user
    customer = get_or_create_customer(user)
    open_orders=Order.objects.filter(customer=customer, complete_order=False)
    
    if open_orders.exists():
        order = open_orders.first()
        order_items=OrderItem.objects.filter(order=order)
        
        # total_cart_items = order.get_cart_items
        # total_cart_price = order.get_cart_total
        
        # for item in order_items:
        #     print(item.book.name, item.quantity)
        
        # print("Cart Items:", order.get_cart_items)
        # print("Cart Total:", order.get_cart_total)
    else:
        order=None
        order_items=[]
        
    return {'order_items' : order_items, }