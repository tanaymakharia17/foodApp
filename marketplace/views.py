from django.shortcuts import render, get_object_or_404
from vendor.models import Vendor
from django.http import HttpResponse, JsonResponse
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from .models import Cart
from .context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required
# Create your views here.



def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset= FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    # print(cart_items)
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if is_ajax(request):
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                
                # Check if the user has already added food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})

                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'Added the food to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})

            except:
                return JsonResponse({'status': 'failed', 'message': 'This food dosen\'t exist'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request'})
            # return JsonResponse({'status': 'success', 'message': 'user is loggedin'})
    return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


# @login_required(login_url='login')
def decrease_cart(request, food_id=None):
    if request.user.is_authenticated:
        if is_ajax(request):
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                
                # Check if the user has already added food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    chkCart.quantity -= 1
                    if chkCart.quantity >= 1:
                        chkCart.save()
                    else:
                        chkCart.delete()
                    return JsonResponse({'status': 'success', 'message': 'Decreased the item quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})

                except:
                    return JsonResponse({'status': 'failed', 'message': 'This item is not in your cart'})

            except:
                return JsonResponse({'status': 'failed', 'message': 'This food dosen\'t exist'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request'})
            # return JsonResponse({'status': 'success', 'message': 'user is loggedin'})
    return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})



@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items
    }
    return render(request, 'marketplace/cart.html', context)


@login_required(login_url='login')
def delete_cart(request, cart_id):

    if request.user.is_authenticated:
        if is_ajax(request):
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'success', 'message': 'Item has been deleted!', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'failed', 'message': 'Cart item dosen\'t exist!'})
 
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request'})


    return JsonResponse({'status': 'login_required', 'message': 'Invalid request'})


