"""Url paths for lead app."""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('success/', views.PaymentSuccessView.as_view(), name='success'),
    path('superuser/list/', views.PaymentListView.as_view(), name='admin_list'),
]
