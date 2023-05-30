from django import forms
from .models import Order, Payment, OrderedFood



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'country', 'pin_code']
    
    