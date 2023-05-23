from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from accounts.forms import UserProfileForm
from .forms import VendorForm
from .models import Vendor
from accounts.models import UserProfile
from django.forms.models import model_to_dict
from django.contrib import messages


def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):

    vendor = get_object_or_404(Vendor, user=request.user)
    # vendor = model_to_dict(vendor)
    profile = get_object_or_404(UserProfile, user=request.user)
    # profile = model_to_dict(profile)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Details Updated!")
            return redirect('vprofile')
        else:
            messages.error(request, "Invalid upload! ")
            print(profile_form.errors)
            print(vendor_form.errors)    

    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form
    }
    return render(request, 'vendor/vprofile.html', context)


