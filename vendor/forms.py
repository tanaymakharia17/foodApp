from django import forms
from .models import Vendor

class VendorForm(forms.ModelForm):

    class Meta:
        model = Vendor
        fields = ['vender_name', 'vendor_license']

