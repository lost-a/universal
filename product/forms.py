from django import forms
from django.db.models import fields
from .models import Product,phone,Purchase

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=('name','description','rating','regular','sale','days','location','state','country','tags','itenary','duration_type','loca_city','adventuretype',)

class UpdateForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=('description','rating','regular','sale','days','location','state','country','itenary','duration_type','loca_city','adventuretype',)

class Addphone(forms.ModelForm):
    class Meta:
        model=phone
        fields=('phone',)

class purchaseform(forms.ModelForm):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    class Meta:
        model=Purchase
        fields=('date',)