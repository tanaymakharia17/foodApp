from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

from vendor.models import Vendor

def home(request):
    # print(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT), '-----------------------')
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    print(vendors)
    context = {
        'vendors': vendors
    }
    return render(request, 'home.html', context)
