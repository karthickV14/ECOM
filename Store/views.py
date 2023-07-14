from django.http import  JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from .models import *

from .forms import SignUpForm


# Create your views here.

def index(request):
    category = Category.objects.filter(status=0)
    context = {'category':category}
    return render(request, "Store/index.html",context)


def collections(request):
    category = Category.objects.filter(status=0)
    context = {'category':category}
    return render(request, "Store/collections.html",context)


def collectionsview(request, slug):
    if(Category.objects.filter(slug=slug, status=0)):
        product = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        context = {'product':product, 'category':category}
        return render(request, "Store/collectionsview.html", context)
    else:
        messages.warning(request,"No such Category Found")
        return redirect('collections')

def productview(request,cate_slug, prod_slug):
    if(Category.objects.filter(slug=cate_slug, status=0)):
        if(Product.objects.filter(slug=prod_slug, status=0)):
            products= Product.objects.filter(slug=prod_slug, status=0).first()
            context={'products':products}
        else:
            messages.warning(request,"No such product Found")
            return redirect('collections')
    else:
        messages.warning(request,"No such category Found")
        return redirect('collections')
    return render(request, "Store/productview.html",context)


def register(request):
    form = SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registered successfully")
            return redirect('login')
    context={'form':form}
    return render(request, 'auth/register.html',context)

def login_user(request):
    if request.user.is_authenticated:
        messages.warning(request,"you are already logged in")
        return redirect('/')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"Loggedin successfully")
                return redirect('index')
            else:
                messages.error(request,"Invalid Authentication")
                return redirect('login')

        return render(request,"auth/login.html")
    
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been Logged Out...")
        return redirect('index')
    

def add_to_cart(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            product_id=int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=product_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id,product_id=product_id)):
                    return JsonResponse({'status':"Product Already in Cart"})
                else:
                    product_qty=int(request.POST.get('product_qty'))

                    if product_check.quantity >= product_qty:
                        Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'status':"Product added successfully"})
                    else:
                        return JsonResponse({'status':"Only"+ str(product_check.quantity)+" quantity available"})      
            else:
                return JsonResponse({'status':"No such product found"})
        else:
            return JsonResponse({'status':"Login to Continue"})

    return redirect('/')


@login_required(login_url='login')
def cart(request):
    cart=Cart.objects.filter(user=request.user)
    context= {'cart':cart}
    return render(request,'Extra/cart.html',context)


def updateCart(request):
    if request.method=='POST':
        prod_id=int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user,product_id=prod_id)):
            prod_qty=int(request.POST.get('product_qty'))
            cart=Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty= prod_qty
            cart.save()
            return JsonResponse({'status':"Updated successfully"})
    return redirect('/')


def deleteCartItem(request):
    if request.method=='POST':        
        prod_id=int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user,product_id=prod_id)):
            cartitem= Cart.objects.get(product_id=prod_id,user=request.user)
            cartitem.delete()
            return JsonResponse({'status':"Deleted successfully"})
    return redirect('/')


def productlist(request):
    products=Product.objects.filter(status=0).values_list('name', flat=True)
    productlist=list(products)

    return JsonResponse(productlist, safe=False)

def searchproduct(request):
    if request.method =='POST':
        searchitem = request.POST.get('productsearch')
        if searchitem == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains=searchitem).first()

            if product:
                return redirect('collections/'+product.category.slug+'/'+product.slug)
            else:
                messages.info(request,'No product mached your search')
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))