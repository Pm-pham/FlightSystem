from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Trang chủ
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('terms/', views.terms_and_conditions, name='terms')
]