from django.shortcuts import render,redirect
from users_app.forms import CustomRegistrationForm
from django.contrib import messages
from book_app.models import Customer

# Create your views here.

def register(request):
    if request.method=='POST':
       register_form=CustomRegistrationForm(request.POST)
       if register_form.is_valid():
           user=register_form.save()
           name=register_form.cleaned_data['firstname']
           email=register_form.cleaned_data['email']
           customer=Customer(user=user, name=name, email=email)
           customer.save()
           messages.success(request,("Registration Successful!"))
           return redirect('login') 
    else:
        register_form=CustomRegistrationForm()
    return render(request, 'register.html', {'register_form' : register_form})