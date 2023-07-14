import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, Profile, Cart

from django.contrib.auth.models import User

from .models import Product, Wishlist


@login_required(login_url='login')
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context={'wishlist':wishlist}
    return render(request,'Extra/wishlist.html',context)


def addingWishlist(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check=Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status':"Product Already In Wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status':"Product added to Wishlist"})
            else:
                return JsonResponse({'status': "No such Product Found"})            
        else:
            return JsonResponse({'status':"Loggin To continue"})
    return redirect('/')


def deleteWistItem(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                wistitem = Wishlist.objects.get(product_id=prod_id)
                wistitem.delete()
                return JsonResponse({'status':"Product Removed From Wishlist"})
            else:
                Wishlist.objects.create(user=request.user, product_id=prod_id)
                return JsonResponse({'status':"Product not found in Wishlist"})
        else:
                return JsonResponse({'status': "No such Product Found"})
    return redirect('/')


@login_required(login_url='login')
def checkout(request):
    receive=Cart.objects.filter(user=request.user)
    for item in receive:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)

    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.selling_price * item.product_qty

    userprofile = Profile.objects.filter(user=request.user).first()

    context={'cartitems':cartitems, 'total_price':total_price,'userprofile':userprofile}
    return render(request, 'Extra/checkout.html', context)



@login_required(login_url='login')
def placeorder(request):
    if request.method=='POST':

        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile= Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

        neworder=Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')

        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        cart = Cart.objects.filter(user=request.user)
        catr_total_price = 0
        for item in cart:
            catr_total_price = catr_total_price + item.product.selling_price * item.product_qty


        neworder.total_price = catr_total_price
        trackno = 'karthick' + str(random.randint(111111,998877))
        while Order.objects.filter(traking_no = trackno) is None:
            trackno = 'karthick' + str(random.randint(111111,998877))

        neworder.traking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order = neworder,
                product= item.product,
                price = item.product.selling_price,
                quantity = item.product_qty,
            )
            
            orderproduct = Product.objects.filter(id = item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()

        Cart.objects.filter(user=request.user).delete()
        messages.success(request,"Your Order Has Been Placed Success")

        payMode = request.POST.get('payment_mode')
        if(payMode == "Pay Razorpay"):
            return JsonResponse({'status': "Your Payment Is Successfully Placed"})
    return redirect('/')


@login_required(login_url='login')
def razerpay(request):
    cart= Cart.objects.filter(user=request.user)
    total_price=0
    for item in cart:
        total_price=total_price + item.product.selling_price * item.product_qty

    return JsonResponse({
        'total_price':total_price
    })



def orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders':orders}
    return render(request, "Extra/order.html", context)

def orderview(request,t_no):
    order = Order.objects.filter(traking_no=t_no).filter(user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {'order':order,'orderitems':orderitems}
    return render(request, "Extra/vieworder.html", context)