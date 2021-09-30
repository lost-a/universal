from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Destination(models.Model):
    name=models.CharField(max_length=50)
    type = models.CharField(max_length=200, choices=Type_CHOICES, default='',null=True,blank=True)
    statename=models.CharField(max_length=200,default='',null=True, blank=True)
    order=models.IntegerField(default=0,null=True, blank=True)
    covid_status=models.CharField(max_length=1000,default="",null=True,blank=True)
    how_to_reach=models.CharField(max_length=1000,default="",null=True,blank=True)
    weather=models.CharField(max_length=1000,default="",null=True,blank=True)
    weather_javascript=models.CharField(max_length=1000,default="",null=True,blank=True)
    image= models.ImageField(upload_to='uploads/products/',null=True,blank=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    name= models.CharField(max_length=200,default="",null=True,blank=True) 
    description=models.CharField(max_length=2000,default="",null=True,blank=True)
    rating=models.IntegerField(default=0,null=True,blank=True)
    regular=models.IntegerField(default=0,null=True,blank=True)
    sale=models.IntegerField(default=0,null=True,blank=True)
    days=models.IntegerField(default=0,null=True,blank=True)
    location=models.CharField(max_length=50,default="",null=True,blank=True)
    slug=models.SlugField(unique=True,null=True,blank=True)
    state=models.CharField(max_length=50,default="",null=True,blank=True)
    country=models.CharField(max_length=50,default="",null=True,blank=True)
    itenary=models.CharField(max_length=10000,default="",null=True,blank=True)
    duration_type=models.CharField(max_length=100,default="",null=True)
    loca_city=models.CharField(max_length=2000,default="",null=True)
    adventuretype=models.CharField(max_length=50,default="",null=True)
    tags=TaggableManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products", kwargs={"slug": self.slug})

class des(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    description=models.CharField(max_length=1000,default="",blank=True,null=True)
   
class Images(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    image= models.ImageField(upload_to='uploads/products/',null=True,blank=True)
 
 
class duration(models.Model):
    name=models.CharField(max_length=50,default="");
    def __str__(self):
        return self.name

class Countries(models.Model):
    name=models.CharField(max_length=50,default="")
    def __str__(self):
        return self.name



class states(models.Model):
    Country=models.ForeignKey(Countries,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,default="")
    image=models.ImageField(upload_to='uploads/products/',null=True,blank=True)
    def __str__(self):
        return self.name


class Tags(models.Model):
    name=models.CharField(max_length=50,default="")
    def __str__(self):
        return self.name


class phone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    phone=models.CharField(null=False,default="",max_length=10)
    def __str__(self):
        return self.phone


class Purchase(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.CharField(max_length=50,null=True)
    date=models.DateField(null=True,auto_now=False,auto_now_add=False)
    days=models.IntegerField(null=True,default=1)
    orderId=models.CharField(null=True,max_length=100)
    orderAmount=models.CharField(null=True,max_length=50)
    referenceId=models.CharField(null=True,max_length=100)
    created=models.DateTimeField(null=True, auto_now=True, auto_now_add=False,blank=True)
    def __str__(self):
        return self.orderId



def pre_save_post_reciever(sender,instance,*args, **kwargs):
    slug=slugify(instance.name)
    exists=Product.objects.filter(slug=slug).exists()
    if exists:
        slug="%s-%s"%(slugify(instance.name),instance.id)
    instance.slug=slug

pre_save.connect(pre_save_post_reciever,sender=Product)
