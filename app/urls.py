from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('qui-sommes-nous/', views.about, name='about'),
    path('galerie/', views.gallery, name='gallery'),
    path('faire-un-don/', views.donate, name='donate'),
    path('contact/', views.contact, name='contact'),
    path('domaines/<slug:slug>/', views.domain_detail, name='domain_detail'),
]
