import razorpay
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.db import transaction
from .models import *
from .forms import CheckoutForm
from .utils import *
# Create your views here.


def index(request):
    content= { 'index_text':"Welcome to Home Page!",
        }
    
    return render(request, 'index.html', content)

def book_list(request):
    
    books=Book.objects.all()
    return render(request, 'book_list.html', {'books' : books})

def book_detail(request, pk):
  book = get_object_or_404(Book, pk=pk)
  return render(request, 'book_detail.html', {'book': book})

@login_required
def add_to_cart(request, pk):
    
    user = request.user
    customer = get_or_create_customer(user)
    book = get_object_or_404(Book, pk=pk)
    order,created=Order.objects.get_or_create(customer=customer,complete_order=False)
    order_item,item_created=OrderItem.objects.get_or_create(order=order, book=book)
    if order_item.quantity is None:
        order_item.quantity = 0  # Initialize to zero or another default value
    order_item.quantity +=1
    order_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request,pk):
    user = request.user
    customer = get_or_create_customer(user)
    book = get_object_or_404(Book, pk=pk)
    order_item=OrderItem.objects.filter(order__customer=customer,book=book).first()
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order_item.delete()
    return redirect('cart')

@login_required    
def cart(request):
    
    data=orderData(request)
    order_items=data['order_items']
    total_cart_items=0
    if 'order_items' in data:
        total_cart_items=sum(item.quantity for item in data['order_items'])
        
    total_cart_price=0
    if 'order_items' in data:
        total_cart_price=sum(item.get_price for item in data['order_items'])
            
    context={'order_items' : order_items, 'total_cart_items' : total_cart_items, 'total_cart_price': total_cart_price, }
    
    if request.method == 'POST' and 'checkout' in request.POST:
        # Assuming you have a function to process the payment and create an order
        order = process_payment(request.user, order_items, total_cart_price)
        if order:
            # Clear the cart items associated with the current user
            if 'order_items' in request.session:
                del request.session['order_items']
            # Redirect to a thank you or order confirmation page
            return redirect('cart')
    return render(request,'cart.html', context)
    
@login_required
def checkout(request):
    user = request.user
    customer = get_or_create_customer(user)
    data = orderData(request)
    order_items = data.get('order_items', [])

    total_cart_items = sum(item.quantity for item in order_items)
    total_cart_price = sum(item.get_price for item in order_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            shipping_address = form.cleaned_data['shipping_address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']

            order, created = Order.objects.get_or_create(customer=customer, complete_order=False)

            shipping_address_obj = ShippingAddress(
                customer=customer,
                order=order,
                address=shipping_address,
                city=city,
                state=state,
                pincode=pincode
            )
            shipping_address_obj.save()

            try:
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                payment = client.order.create({
                    'amount': int(total_cart_price * 100),  # Ensure amount is in paise
                    'currency': 'INR',
                    'payment_capture': '1'
                })
                order.razor_pay_order_id = payment['id']
                order.save()
                print('Payment:', payment)
                return render(request, 'checkout.html', {'payment': payment})
            except Exception as e:
                # Handle payment initiation errors
                print('Payment initiation failed:', e)
                form.add_error(None, 'Payment initiation failed. Please try again.')

    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'order_items': order_items,
        'total_cart_items': total_cart_items,
        'total_cart_price': total_cart_price,
    }
    return render(request, 'checkout.html', context)

def process_payment(request,order_id):
    print("Received order_id:", order_id)
    
    if request.method =="POST":
        
        razorpay_order_id=request.POST.get('razorpay_order_id')
        razorpay_payment_id=request.POST.get('razorpay_payment_id')
        razorpay_signature=request.POST.get('razorpay_signature')
        
        client=razorpay.Client(auth= (settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        params_dict={
            'razorpay_order_id' : razorpay_order_id,
            'razorpay_payment_id' : razorpay_payment_id,
            'razorpay_signature' : razorpay_signature,
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
            
            order = get_object_or_404(Order, pk=order_id)
            print("Order Object:", order)
            print("Order Status (before update):", order.complete_order)
            
            order.transaction_id=order.generate_transaction_id
            order.complete_order=True
            order.save()
            
            print("Order Status (after update):", order.complete_order)
            
            return HttpResponse('Payment Successful')

        except Exception as e:
            return HttpResponse('Payment Failed')

def contact(request):
    content= { 'index_text':"Welcome to Contact Page!",
        }
    
    return render(request, 'contact.html', content)

def about(request):
    content= { 'index_text':"Welcome to About Page!",
        }
    
    return render(request, 'about.html', content)

