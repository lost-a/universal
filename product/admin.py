from django.contrib import admin
from .models import Product,Countries,states,Destination,Images,phone,Purchase,duration

admin.site.register(Product)
admin.site.register(Destination)
admin.site.register(Images)
admin.site.register(states)
admin.site.register(phone)
admin.site.register(Purchase)
admin.site.register(duration)
# Register your models here.
