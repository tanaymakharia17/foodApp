from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from accounts.forms import UserProfileForm
from .forms import VendorForm
from .models import Vendor
from accounts.models import UserProfile
from django.forms.models import model_to_dict
from django.contrib import messages
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify


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



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')

    context = {
        'categories': categories
    }
    return render(request, 'vendor/menu_builder.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk):
    vendor = Vendor.objects.get(user=request.user)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category).order_by('created_at')
    # fooditems = FoodItem.objects.filter(category__pk=pk)
    print(fooditems)
    context = {
        'fooditems': fooditems,
        'category': category
    }
    return render(request, 'vendor/fooditems_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):


    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = Vendor.objects.get(user=request.user)
            
            category.save()
            category.slug = slugify(category_name)+'-'+str(category.id)
            messages.success(request, "Category added successfully!")
            return redirect('menu_builder')
        else:
            messages.error(request, "Thier was some problem. Please try again!")
    else:
        form = CategoryForm()
    context = {
        'form': form
    }
    return render(request, 'vendor/add_category.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = Vendor.objects.get(user=request.user)
            category.slug = slugify(category_name)
            form .save()
            messages.success(request, "Category added successfully!")
            return redirect('menu_builder')
        else:
            messages.error(request, "Thier was some problem. Please try again!")
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'vendor/edit_category.html', context)




@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category is deleted successfully!')

    return redirect('menu_builder')



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            foodTitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = Vendor.objects.get(user=request.user)
            form.save()
            messages.success(request, 'Food Item added successfully!')
            return redirect('fooditems_by_category', food.category.id)
    else:
        form = FoodItemForm()
    context = {
        'form': form
    }
    form.fields['category'].queryset = Category.objects.filter(vendor=Vendor.objects.get(user=request.user))
    return render(request, 'vendor/add_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = Vendor.objects.get(user=request.user)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request, "Food Item updated successfully!")
            return redirect('fooditems_by_category', food.category.id)
        else:
            messages.error(request, "Thier was some problem. Please try again!")
    else:
        form = FoodItemForm(instance=food)
    
    form.fields['category'].queryset = Category.objects.filter(vendor=Vendor.objects.get(user=request.user))
    context = {
        'form': form,
        'food': food
    }
    return render(request, 'vendor/edit_food.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, pk):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, 'Food Item is deleted successfully!')

    return redirect('fooditems_by_category', food.category.id)

