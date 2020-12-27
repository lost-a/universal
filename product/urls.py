from os import name
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<slug:slug>/',views.product,name='product'),
    path('destination/<slug:slug>/',views.destination,name='destination'),
    path('handlerequest/',views.cash,name='cash'),
    path('checkout/',views.checkout,name='checkout'),
    path('add/',views.ProductCreate,name='productcreate'),
    path('profile/',views.profile,name='profile'),
    path('download/<slug:slug>/',views.download,name='download'),
    path('product/all/',views.more,name='more'),
    path('ajax_calls/search/',views.autocompleteModel,name='autocompleteModel'),
    path('search',views.search,name='search'),
    path('admin_route/',views.adminr,name='admins'),
    path('tag/<slug:tag_slug>',views.Tagged,name='tagged_product'),
    path('update/<slug:slug>/',views.ProductUpdate,name='up'),
    path('delete/<slug:slug>/',views.DeleteImg,name='del'),
    path('privacy-policy/',views.Privacy,name='privacy'),
]