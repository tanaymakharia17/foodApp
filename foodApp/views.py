from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static



def home(request):
    # print(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT), '-----------------------')
    return render(request, 'home.html')
