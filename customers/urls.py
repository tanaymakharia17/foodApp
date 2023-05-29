

from django.urls import path
from accounts import views as AccountsViews

from . import views

urlpatterns = [
    path('', AccountsViews.custDashboard, name='customer'),
    path('profile/', views.cprofile, name='cprofile'),
]