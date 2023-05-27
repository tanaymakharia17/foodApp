from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from vendor.models import Vendor



def get_or_set_current_location(request):
    if 'lat' in request.GET and 'lng' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        request.session['lat'] = lat
        request.session['lng'] = lng
        return lng, lat
    elif 'lat' in request.session and 'lng' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lng, lat
    else:
        return None

def home(request):
    if get_or_set_current_location(request) is not None:
        # lat = request.GET.get('lat')
        # lng = request.GET.get('lng') # [TODO] - Add validation for lat and lng
        lng, lat = get_or_set_current_location(request)
        pnt = GEOSGeometry('POINT(%s %s)' % (lng, lat), srid=4326)

        vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt, D(km=1000))).annotate(distance=Distance('user_profile__location', pnt)).order_by('distance')[:8]
        print(vendors)

        for v in vendors:
            v.kms = round(v.distance.km, 2)
            if v.kms == 0.00:
                v.kms = 0.01
    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    context = {
        'vendors': vendors
    }
    return render(request, 'home.html', context)
