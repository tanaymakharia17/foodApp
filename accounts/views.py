from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from .utils import detectUser, send_verification_email, send_password_reset_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
from django.template.defaultfilters import slugify
from orders.models import Order
# from foodApp.views import home
import datetime
# Restrict the vendor from accessing the cusomer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restrict the cusomer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in !")
        return redirect('myAccount')
    if request.method == 'POST':
        form = UserForm(request.POST)
        context = {}
        if form.is_valid():
            # create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False) # or form.save()
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            # create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()

            # Send verificaion email
            send_verification_email(request, user)

            messages.success(request, "Your account have been registered successfully")
            return redirect('registerUser')
        else:
            print(form.errors)
            messages.error(request, "Your account is not created, Please try again!")
            return render(request, 'accounts/registerUser.html', context={'form':form})
            # return HttpResponse('error')

        

    form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/registerUser.html', context)
    return HttpResponse('hello')



def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in !")
        return redirect('myAccount')
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.vendor_slug = slugify(v_form.cleaned_data['vender_name'])+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # Send verificaion email
            send_verification_email(request, user)

            messages.success(request, "Your account creation request sent successfully")
            return redirect('registerVendor')
        else:
            messages.error(request, "Account not created, Try again")
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form': form,
        'v_form': v_form
    }
    return render(request, 'accounts/registerVendor.html', context)



def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in !")
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return myAccount(request)
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
        
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out')
    return redirect('login')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    recent_orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    orders_count = recent_orders.count()

    recent_orders = recent_orders[:5]
    context = {
        'recent_orders': recent_orders,
        'orders_count': orders_count
    }
    return render(request, 'accounts/custDashboard.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor = Vendor.objects.get(user=request.user)
    # print(vendor)
    orders = Order.objects.filter(vendors__in=[vendor.pk], is_ordered=True).order_by('-created_at')
    # print(orders)
    current_month = datetime.datetime.now().month
    current_month_orders = orders.filter(vendors__in=[vendor.id], created_at__month=current_month)
    current_month_revenue = 0
    for i in current_month_orders:
        current_month_revenue += i.get_total_by_vendor()['grand_total']


    total_revenue = 0
    for i in orders:
        total_revenue += i.get_total_by_vendor()['grand_total']
    orders_count = orders.count()
    print(orders)
    context = {
        'vendor': vendor,
        'orders': orders,
        'orders_count': orders_count,
        'recent_orders': orders[:5],
        'total_revenue': total_revenue,
        'current_month_revenue': current_month_revenue
    }
    return render(request, 'accounts/vendorDashboard.html', context)


@login_required(login_url='login')
def myAccount(request):
    # if not request.user.is_authenticated:
    #     messages.warning(request, "You are not logged in !")
    #     return redirect('login')
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your Account is authenticated and activated")
    else:
        messages.error(request, "Invalid acttivation link")

    return redirect('myAccount')


    # Activate the user by setting the is_active status to true

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # send reset Password email
            send_password_reset_email(request, user)
            messages.success(request, 'Passwoed reset link sent to your email address.')
            redirect('login')
        else:
            messages.error(request, "Account Dosen't exist")
            redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session['uid']
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successfull')
            return redirect('login')
        else:
            messages.error(request, "Password do not match !")
            return redirect('resetPassword')
    return render(request, 'accounts/resetPassword.html')

def resetPasswordValidate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired')

    return redirect('myAccount')
    return render(request, 'accounts/resetPassword.html')