from django.shortcuts import render, redirect
from homeuser.views import usershop 
from orders.models import Orders, OrderProduct
from cart.models import Cart, CartItem, Address
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product, SizeVariant ,Category
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def usercart(request ,total = 0, cartitems = None ):
    category = Category.objects.all()
    if request.user.is_authenticated:
        cartitems = CartItem.objects.filter(user=request.user , is_active = True).order_by("-id")
        total = 0
        for cart_item in cartitems:
            total += (cart_item.cartprice * cart_item.quantity)
        context = {'login': 'login', 'cartitems': cartitems, 'total': total ,'category': category}
        # return render(request, 'userpages/usercart.html', context)
    else:
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart.save()
            cartitems = CartItem.objects.filter(cart=cart , is_active = True).order_by("-id")
            for cart_item in cartitems:
                total += (cart_item.cartprice * cart_item.quantity)
            print('it total')
            print(total)
        except ObjectDoesNotExist:
            pass  # just ignore
        context = {'cartitems': cartitems, 'total': total ,'category': category}
    return render(request, 'userpages/usercart.html', context)
        # return redirect(logins)


def _cart_id(request):
    session_id = request.session.session_key
    if not session_id:
        session_id = request.session.create()
    return session_id

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_cart(request):
    if request.method == 'POST':
        product_slug = request.POST.get('product_slug')
        size = request.POST.get('size')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(slug =product_slug)  # get the product
        sizevariantm = SizeVariant.objects.get(uid = size)

        if sizevariantm.Stock < 1:
            messages.warning(request, 'Out of Stock, choose difrent size Variant.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if request.user.is_authenticated:
            try:
                cart_item = CartItem.objects.get(product=product, user=request.user ,sizemodel = sizevariantm )
                cart_item.quantity += int(quantity)
                cart_item.cartprice = int(price)
                cart_item.save()

            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(
                product=product, quantity=quantity, user=request.user, sizemodel=sizevariantm , cartprice = price )
                cart_item.save()
        else:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request)) #get the cart using the cartid present in the session
            except Cart.DoesNotExist:
                cart = Cart.objects.create(cart_id = _cart_id(request))
                cart.save()
            try:
                cart_item = CartItem.objects.get(product = product, cart = cart ,sizemodel = sizevariantm)
                cart_item.quantity += int(quantity) 
                cart_item.cartprice += int(price) 
                cart_item.save()

            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(product = product,quantity = quantity, cart = cart,sizemodel=sizevariantm , cartprice = price)
                cart_item.save()
        return redirect(usershop)
    return redirect(usershop)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletecart_item(request, cart_id):
    thiscartitem = CartItem.objects.get(id = cart_id)
    thiscartitem.delete()
    return redirect(usercart)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updatecart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                new_quantity = request.POST.get(f'{item.id}')
                if new_quantity and new_quantity != item.quantity:
                    item.quantity = new_quantity
                    item.save()
            return redirect(usercart)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart = cart)
            for item in cart_items:
                new_quantity = request.POST.get(f'{item.id}')
                if new_quantity and new_quantity != item.quantity:
                    item.quantity = new_quantity
                    item.save()
            return redirect(usercart)
    return redirect(usercart)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def orderdetails(request,id):
    category = Category.objects.all()
    orderprod = OrderProduct.objects.filter(order = id).order_by('-id')
    context = {'orderprod':orderprod , 'login':'login' ,'category': category}
    return render (request,'userpages/orderdetails.html',context )


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ordercancel(request,id):
    print(request.user)
    order = OrderProduct.objects.get(id = id )
    order.status = 'Cancelled'
    order.save()
    order.sizevariant.Stock +=order.quantity
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def wishlist(request ,total = 0, cartitems = None):
    category = Category.objects.all()
    if request.user.is_authenticated:
        cartitems = CartItem.objects.filter(user=request.user ,is_active = False ).order_by("-id")
        total = 0
        for cart_item in cartitems:
            total += (cart_item.cartprice * cart_item.quantity)
        context = {'login': 'login', 'cartitems': cartitems, 'total': total ,'category': category}
        # return render(request, 'userpages/usercart.html', context)
    else:
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart.save()
            cartitems = CartItem.objects.filter(cart=cart ,is_active = False ).order_by("-id")
            for cart_item in cartitems:
                total += (cart_item.cartprice * cart_item.quantity)
            print('it total')
            print(total)
        except ObjectDoesNotExist:
            pass  # just ignore
        context = {'cartitems': cartitems, 'total': total ,'category': category}
    return render(request, 'userpages/wishlist.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_wishlist(request ,cart_id):
    thiscartitem = CartItem.objects.get(id = cart_id)
    thiscartitem.is_active = False
    thiscartitem.save()
    return redirect(usercart)

def add_direct_wishlist(request ,slug):
    product = Product.objects.get(slug=slug)
    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product=product, user=request.user, is_active = False )
            cart_item.quantity += 1
            cart_item.cartprice = product.price
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
            product=product, quantity=1, user=request.user, cartprice = product.price , is_active = False )
            cart_item.save()
    else:
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request)) #get the cart using the cartid present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()
        try:
            cart_item = CartItem.objects.get(product = product, cart = cart , is_active = False)
            cart_item.quantity += 1
            cart_item.cartprice += product.price
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1, cart = cart, is_active = False  , cartprice = product.price)
            cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))






# useraccount.html