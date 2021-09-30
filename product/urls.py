from os import name
from django.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index'),
    path('products/<slug:slug>/',views.product,name='product'),
    path('productimages/<slug:slug>/',views.images,name='images'),
    path('destination/',views.destination,name='destination'),
    path('filter-data/',views.FilterData,name='filter-data'),
    path('add/',views.ProductCreate,name='productcreate'),
    path('profile/',views.profile,name='profile'),
    path('ajax_calls/search/',views.autocompleteModel,name='autocompleteModel'),
    path('search/',views.search,name='search'),
    path('autosuggest/',views.autosuggest,name='autosuggest'),
    path('admin_route/',views.adminr,name='admins'),
    path('tag/<slug:tag_slug>',views.Tagged,name='tagged_product'),
    path('update/<slug:slug>/',views.ProductUpdate,name='up'),
    path('delete/<slug:slug>/',views.DeleteImg,name='del'),
    path('privacy-policy/',views.Privacy,name='privacy'),
    path('adventure/<slug:slug>/',views.Adventure,name='adventure'),
    path('tour/<slug:slug>/',views.Tour,name='tour'),
    path('city/<slug:slug>/',views.City,name='city'),
    path('state/<slug:slug>/',views.State,name='state'),
    path('partial-payment/',views.Partial,name='partial-payment'),
    path('producttype/',views.prodtype,name='producttype'),
    path('refund-policy/',views.Refund,name='refund-policy'),
    path('about/', views.About, name="about"),
    path('contact/', views.Contact, name="contact"),
    url(r'^delete2/(?P<pk>[0-9]+)/$', views.Delete, name='delete_view'),
    url(r'^delete3/(?P<pk>[0-9]+)/$', views.Delete2, name='delete_view2'),
    path('itinerary_response/<slug:slug>', views.Response_Itinerary, name='Itinerary_response'),
]
