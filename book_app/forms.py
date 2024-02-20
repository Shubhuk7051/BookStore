from django import forms

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=50, required=True)
    state = forms.CharField(max_length=50, required=True)
    pincode = forms.CharField(max_length=10, required=True)