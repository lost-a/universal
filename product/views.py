import hashlib
import uuid 
import hmac
import base64
from django.db.models import query
from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from .models import Product,Destination,Images, phone,Purchase,states,des
from .forms import ProductForm,Addphone,purchaseform,UpdateForm
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth.models import User
import datetime
from taggit.models import Tag
import json
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    context ={
        'products' : Product.objects.all(),
        'destinations':Destination.objects.all()
    }
    return render(request,'index.html',context)




def more(request):
    Products=Product.objects.all()

    if request.method=='POST':
        rangef=request.POST.get('range')
        advent=request.POST.get('adventure')
        dur=request.POST.get('duration')
        if rangef=="1":
            if (advent==None or advent=="All") and dur ==None:
                Products=Product.objects.all()

            elif advent==None or advent=="All":
                Products=Product.objects.filter(duration_type=dur)

            elif dur==None:
                Products=Product.objects.filter(adventuretype=advent)
            
            else:
                Products=Product.objects.filter(adventuretype=advent).filter(duration_type=dur)
        
        else:
            if (advent==None or advent=="All") and dur ==None:
                Products=Product.objects.all().filter(sale__range=(0,rangef))

            elif advent==None or advent=="All":
                Products=Product.objects.filter(duration_type=dur).filter(sale__range=(0,rangef))

            elif dur==None:
                Products=Product.objects.filter(adventuretype=advent).filter(sale__range=(0,rangef))
            
            else:
                Products=Product.objects.filter(adventuretype=advent).filter(duration_type=dur).filter(sale__range=(0,rangef))

    context ={
        'products' : Products,
        
    }
    return render(request,'more.html',context)




def search(request):
    query=request.GET['query']
    if(len(query)>78):
        product=[]
    else:
        title=Product.objects.filter(name__icontains=query)
        state=Product.objects.filter(state__icontains=query)
        data=Product.objects.filter(description__icontains=query)
        product=title.union(state)
        product=product.union(data)
        
    context ={
        'products' :product ,
        'query':query
    }
    return render(request,'more.html',context)

def Tagged(request,tag_slug):
    
    tag=get_object_or_404(Tag,slug=tag_slug)    
    product=Product.objects.filter(tags_in=[tag])
    context ={
        'products' :product ,
        'query':query
    }
    return render(request,'more.html',context)

@api_view(['GET',])
def Tour(request,slug):
    state = request.GET.get('state', '')
    city = request.GET.get('city', '')
    

    if slug == 'all':
        if len(city)>0:
            paginator = Product.objects.filter( category='Tour',city=city)
            place=city
        elif len(state)>0:
            paginator = Product.objects.filter(category='Tour',state=state)
            
        else:
            paginator = Product.objects.filter(category='Tour')
      
    else:
        a=slug.split('-')
        if len(a)>1:
            slug= a[0]+' '+a[1]
        if len(a)>2:
            slug= a[0]+' '+a[1]+' '+a[2]
        if len(city)>0:
            paginator = Product.objects.filter(category='Tour',city=city,tag_category=slug)
        elif len(state)>0:
            paginator = Product.objects.filter(category='Tour',state=state,tag_category=slug)
        else:
            paginator = Product.objects.filter(category='Tour',tag_category=slug)
        
        
    context={'pro':paginator.values()}
    return Response(context['pro'])

def autocompleteModel(request):

    if request.is_ajax():
        q = request.GET.get('term', '')
        state = states.objects.filter(name__icontains=q)
        results = []
        for pl in state:
            product_json={}
            product_json=pl.name
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def profile(request):
    context={
        'purchase':Purchase.objects.all(),
    }
    
    return render(request,'profile.html',context)

def product(request,slug):
    product=get_object_or_404(Product,slug=slug)
    form=Addphone()
    if request.method=='POST':
        current_user = request.user
        phones= phone(user=current_user,phone=request.POST.get('phone'))
        phones.save()
        messages.success(request,"Added")
        return redirect('index')

    context ={
        'product':product,
        'form':form
    }

    return render(request,'product.html',context)

def destination(request,slug):
    context={
        'states':states.objects.filter(name=slug),
        'products':Product.objects.filter(state=slug)
    }
    return render(request,'destination.html',context)
def Privacy(request):
    return render(request,'privacy.html')

def checkout(request):
    if request.method=="POST":
        prod=get_object_or_404(Product,id=request.POST.get('orderid'))
        postData = {
            "appId" : '97514c4ed6f3e88f48c047b61579',
            "orderId" : uuid.uuid4().hex[:6].upper(),
            "orderAmount" : request.POST.get('amount'),
            "orderCurrency" : 'INR',
            "orderNote" : "g",
            "customerName" : request.POST.get('name'),
            "customerPhone" : request.POST.get('phone'),
            "customerEmail" : request.POST.get('email'),
            "returnUrl" : 'https://universaladventures.in/handlerequest/',
            "notifyUrl" : 'https://universaladventures.in/'
        }
        dates=datetime.datetime.strptime(request.POST.get('date'), "%m/%d/%Y").strftime("%Y-%m-%d")
        purchase=Purchase(user=request.user,product=prod,date=dates,days=request.POST.get('number'),orderId=postData["orderId"],orderAmount=request.POST.get('amount'))
        purchase.save()
        sortedKeys = sorted(postData)
        signatureData = ""
        for key in sortedKeys:
            signatureData += key+postData[key];

        message = signatureData.encode('utf-8')
        #get secret key from your config
        secretkey="96d9e9a3801fc8914dde8e92a19ad866302335f5"
        secret = secretkey.encode('utf-8')
        signature = base64.b64encode(hmac.new(secret, message,digestmod=hashlib.sha256).digest()).decode("utf-8")
        postData["signature"]=signature
        return render(request,'checkoutform.html',{'postData':postData})


@csrf_exempt
def cash(request):
    if request.method=="POST":
        postData = {
            "orderId" :  request.POST.get('orderId'), 
            "orderAmount" :  request.POST.get('orderAmount'), 
            "referenceId" :  request.POST.get('referenceId'), 
            "txStatus" :  request.POST.get('txStatus'), 
            "paymentMode" :  request.POST.get('paymentMode'), 
            "txMsg" : request.POST.get('txMsg'), 
            "signature" :  request.POST.get('signature'), 
            "txTime" :  request.POST.get('txTime')
         }
        purc=get_object_or_404(Purchase,orderId=request.POST.get('orderId'))
        purc.status= request.POST.get('txStatus')
        purc.referenceId=request.POST.get('referenceId')
        purc.save()
        signatureData = ""
        signatureData = postData['orderId'] + postData['orderAmount'] + postData['referenceId'] + postData['txStatus'] + postData['paymentMode'] + postData['txMsg'] + postData['txTime']
        message = signatureData.encode('utf-8')

        secretkey="96d9e9a3801fc8914dde8e92a19ad866302335f5"

        secret = secretkey.encode('utf-8')
        computedsignature = base64.b64encode(hmac.new(secret,message,digestmod=hashlib.sha256).digest()).decode('utf-8')   
        context ={
            'postData':postData,
            'computedsignature':computedsignature,
            'purchase':purc
        }

        return render(request,'pdf.html', context)
@staff_member_required           
def adminr(request):
    context={
        'purchases':Purchase.objects.all(),
        'products':Product.objects.all(),
    }
    return render(request,'admins.html',context)

@staff_member_required
def ProductCreate(request):
    ImageFormSet = modelformset_factory(Images,
                                        fields=('image',), extra=4)
    DescriptionFormSet=modelformset_factory(des,fields=('description',),extra=3)
    form = ProductForm()
    if request.method == 'POST':
        form=ProductForm(request.POST)
        formset = ImageFormSet(request.POST or None, request.FILES  or None)
        formset2=DescriptionFormSet(request.POST or None)
        if formset.is_valid() and formset2.is_valid():
            prod= form.save(commit=False)
            prod.save()
            form.save_m2m()
            for f in formset:
                try:
                    photo=Images(product=prod,image=f.cleaned_data['image'])
                    photo.save()
                    
                except Exception as e:
                    break

            for f in formset2:
                try:
                    desc=des(product=prod,description=f.cleaned_data['description'])
                    desc.save()
                except Exception as e:
                    break

            messages.success(request,
                             "Posted!")
            return redirect('index')

        else:
            
            messages.success(request,
                             "error")

    else:
        form = ProductForm()
        formset=ImageFormSet(queryset=Images.objects.none())
        formset2=DescriptionFormSet(queryset=des.objects.none())

    context={
        'form':form,
        'formset':formset,
        'formset2':formset2,

    }
    return render(request,'form.html',context)


def download(request,slug):
    
    detail= get_object_or_404(Purchase,orderId=slug)
    return render(request,'download.html',{'purchase':detail})

    

@staff_member_required
def ProductUpdate(request,slug):
    form = UpdateForm()
    ImageFormSet = modelformset_factory(Images,
                                        fields=('image',), extra=4)
    DescriptionFormSet=modelformset_factory(des,fields=('description',),extra=3)
    product=get_object_or_404(Product,id=slug)
    description=product.description
    itenary=product.itenary
    if request.method == 'POST':
        form= UpdateForm(request.POST or None,instance=product)
        form.save()
        formset = ImageFormSet(request.POST or None, request.FILES  or None)
        formset2=DescriptionFormSet(request.POST or None)
        if request.POST.get('description') == "":
            product.description=description

        if request.POST.get('itenary') == "":
            product.itenary= itenary
        
        product.save()
        if formset.is_valid() and formset2.is_valid():
            for f in formset:
                try:
                    photo=Images(product=product,image=f.cleaned_data['image'])
                    photo.save()
                    
                except Exception as e:
                    break

            for f in formset2:
                try:
                    desc=des(product=product,description=f.cleaned_data['description'])
                    desc.save()
                except Exception as e:
                    break

            return redirect('index')
    else:
        form = UpdateForm()
        formset=ImageFormSet(queryset=Images.objects.none())
        formset2=DescriptionFormSet(queryset=des.objects.none())


    context={
      'product':product,
      'form':form,
      'formset':formset,
      'formset2':formset2,
    }
    return render(request,'update.html',context)

@staff_member_required
def DeleteImg(request,slug):
    image= Images.objects.get(id=slug)
    image.delete()

    return redirect('index')
