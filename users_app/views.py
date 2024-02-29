from django.shortcuts import render,redirect
from django.http import HttpResponse
from users_app.forms import CustomRegistrationForm
from django.contrib import messages
from book_app.models import Customer
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation
from django.core.mail import EmailMessage
from email.mime.text import MIMEText

# Create your views here.

def register(request):
    if request.method=='POST':
       register_form=CustomRegistrationForm(request.POST)
       if register_form.is_valid():
           user=register_form.save()
           name=register_form.cleaned_data['firstname']
           customer_email=register_form.cleaned_data['email']
           customer=Customer(user=user, name=name, email=customer_email)
           customer.is_active=False
           customer.save()
           current_site=get_current_site(request)
           mail_subject="Please Activate Your Account."
           message=render_to_string('verification_mail.html', {
               'user': customer,
               'domain': current_site.domain,
               'uid': urlsafe_base64_encode(force_bytes(customer.pk)),
               'token': account_activation.make_token(customer)
           })

           to_email=register_form.cleaned_data.get('email')
           email=EmailMessage(
                    mail_subject, message, to=[to_email],
           )
           email.content_subtype='html'
           email.send()
        #    send_verification_mail(customer)
           messages.success(request,("Registration Successful!"))
           return HttpResponse('Please confirm your email address to complete the registration')
    else:
        register_form=CustomRegistrationForm()
    return render(request, 'register.html', {'register_form' : register_form})

def activate(request,uidb64, token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user=None
    if user is not None and account_activation.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,("Account is Activated!"))
        return redirect('login')
    else:
        return HttpResponse("Activation Link is invalid!")
        