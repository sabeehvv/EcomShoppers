from django.shortcuts import render, redirect, HttpResponse
from products.models import Product, Category, SizeVariant
from login.views import logins
from cart.models import CartItem, Address
from cart.views import usercart , wishlist
from orders.models import Orders, OrderProduct, Payment
from django.core.paginator import Paginator
import datetime
from django.contrib import messages
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.views.decorators.cache import cache_control
from homeuser.views import usershop
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from login.models import CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


def get_product(request, slug):
    try:
        print(slug)
        category = Category.objects.all()
        product = Product.objects.get(slug=slug)
        return render(request, 'userpages/userproduct.html', context={'product': product, 'category': category})

    except Exception as e:
        print(e)






def checkout(request):
    if request.user.is_authenticated:
        cartitems = CartItem.objects.filter(
            user=request.user, is_active=True).order_by("-id")
        if not cartitems:
            return redirect(usershop)
        for cart_item in cartitems:
            if cart_item.sizemodel.Stock < 1:
                messages.warning(
                    request, 'Move out of stock product into wishlist.')
                return redirect(usercart)
        address = Address.objects.filter(user=request.user).order_by("-id")
        category = Category.objects.all()
        total = 0
        for cart_item in cartitems:
            total += (cart_item.cartprice * cart_item.quantity)
        context = {'login': 'login', 'cartitems': cartitems,
                   'total': total, 'address': address, 'category': category}
        return render(request, 'userpages/checkout.html', context)
    return redirect(logins)


def useraccount(request):
    if request.user.is_authenticated:
        order = Orders.objects.filter(user=request.user).order_by('-id')
        address = Address.objects.filter(user=request.user).order_by("-id")
        category = Category.objects.all()
        p = Paginator(order, 9)
        page = request.GET.get('page')
        orders = p.get_page(page)
        user_wallet = CustomUser.objects.get(email = request.user)
        wallet = user_wallet.wallet

        context = {
            'orders': orders, 'login': 'login', 'address': address, 'category': category , 'wallet':wallet
        }
        return render(request, 'userpages/useraccount.html', context)
    return redirect(logins)


def deleteaddress(request, id):
    thisaddress = Address.objects.get(id=id)
    thisaddress.delete()
    return redirect(useraccount)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addaddress(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        housename = request.POST.get('housename')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        phonenumber = request.POST.get('phonenumber')
        town = request.POST.get('town')

        address = Address(firstname=firstname, lastname=lastname, housename=housename, locality=locality,
                          city=city, state=state, pincode=pincode, phonenumber=phonenumber, town=town, user=request.user)

        address.save()

        return redirect(checkout)
    category = Category.objects.all()
    context = {
        'login': 'login', 'category': category
    }
    return render(request, 'userpages/addaddress.html', context)


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment_confirm(request, total=0, cartitems=None):
    category = Category.objects.all()
    if request.method == "POST":
        if request.user.is_authenticated:
            global thisaddress
            thisaddress = request.POST.get('address')
            if not thisaddress:
                messages.warning(request, 'Add Shipping Address.')
                return redirect(checkout)
            cartitems = CartItem.objects.filter(
                user=request.user, is_active=True).order_by("-id")
            total = 0
            for cart_item in cartitems:
                total += (cart_item.cartprice * cart_item.quantity)
            if total < 1:
                return redirect(usershop)
            currency = 'INR'
            global amounts
            amounts = total * 100

        # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=amounts,
                                                               currency=currency,
                                                               payment_capture='0'))

        # order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            callback_url = 'paymenthandler/'

            context = {'login': 'login', 'cartitems': cartitems, 'razorpay_order_id': razorpay_order_id,
                       'razorpay_merchant_key': settings.RAZOR_KEY_ID, 'razorpay_amount': amounts,
                       'currency': currency, 'callback_url': callback_url,
                       'total': total, 'category': category}
            return render(request, 'userpages/payment.html', context)
        return redirect(logins)
    return redirect(usershop)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ordersend(request):
    cartitems = CartItem.objects.filter(
        user=request.user, is_active=True).order_by("-id")
    if not cartitems:
        return redirect(usershop)
    total = 0
    for cart_item in cartitems:
        total += (cart_item.cartprice * cart_item.quantity)
        # for payment page
    order_id_generated = datetime.datetime.now().strftime(
        '%Y%m%d%H%M%S') + str(random.randint(0, 999)).zfill(3)

    address = Address.objects.get(id=thisaddress)
    paymethod = "COD"
    pay = Payment(
        user=request.user,
        payment_method=paymethod,
        amount_paid=total,
        status="Pending",
    )
    pay.save()

    oder = Orders(user=request.user, address=address,
                  ordertotal=total, orderid=order_id_generated, is_ordered=True, payment=pay)
    oder.save()
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)

    for x in cart_items:
        order = Orders.objects.get(orderid=order_id_generated)
        Orderproduct = OrderProduct(order=order)
        product = Product.objects.get(slug=x.product.slug)
        sizestock = SizeVariant.objects.get(uid=x.sizemodel.uid)
        Orderproduct.product = x.product
        Orderproduct.quantity = x.quantity
        Orderproduct.sizevariant = x.sizemodel
        Orderproduct.price = x.cartprice
        Orderproduct.size = x.sizemodel.size_name
        sizestock.Stock -= x.quantity
        product.save()
        Orderproduct.save()
        sizestock.save()

    for x in cart_items:
        x.delete()

        # order notification
    message = f"New order from {oder.user}. Order Id {oder.orderid}. Order total amount {oder.ordertotal}.Cash on Delivery"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_to_admin",
        {
            'type': 'send_notification',
            'message': json.dumps(message)
        }
    )


    category = Category.objects.all()
    context = {'address': address, 'login': 'login',
               'category': category, 'oder': oder}
    return render(request, 'userpages/ordersend.html', context)



@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = amounts  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment
                    cartitems = CartItem.objects.filter(
                        user=request.user, is_active=True).order_by("-id")
                    if not cartitems:
                        return redirect(usershop)
                    total = 0
                    for cart_item in cartitems:
                        total += (cart_item.cartprice * cart_item.quantity)
                        # for payment page
                    order_id_generated = datetime.datetime.now().strftime(
                        '%Y%m%d%H%M%S') + str(random.randint(0, 999)).zfill(3)

                    address = Address.objects.get(id=thisaddress)

                    pay = Payment(
                        user=request.user,
                        payment_id=payment_id,
                        payment_method="Razorpay",
                        amount_paid=total,
                        status="COMPLETED",
                    )
                    pay.save()
                    oder = Orders(user=request.user, address=address,
                                  ordertotal=total, orderid=order_id_generated, is_ordered=True, payment=pay)
                    oder.save()

                    cart_items = CartItem.objects.filter(
                        user=request.user, is_active=True)
                    for x in cart_items:
                        order = Orders.objects.get(orderid=order_id_generated)
                        Orderproduct = OrderProduct(order=order)
                        product = Product.objects.get(slug=x.product.slug)
                        sizestock = SizeVariant.objects.get(
                            uid=x.sizemodel.uid)
                        Orderproduct.product = x.product
                        Orderproduct.quantity = x.quantity
                        Orderproduct.sizevariant = x.sizemodel
                        Orderproduct.price = x.cartprice
                        Orderproduct.size = x.sizemodel.size_name
                        sizestock.Stock -= x.quantity
                        product.save()
                        Orderproduct.save()
                        sizestock.save()

                    for x in cart_items:
                        x.delete()
                    
                    # order notification
                    message = f"New order from {oder.user}. Order Id {oder.orderid}. Order total amount {oder.ordertotal}. Payment Done"
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        "notification_to_admin",
                        {
                            'type': 'send_notification',
                            'message': json.dumps(message)
                        }
                    )

                    category = Category.objects.all()
                    context = {'address': address, 'login': 'login',
                               'category': category, 'oder': oder}
                    return render(request, 'userpages/ordersend.html', context)

                except:

                    # if there is an error while capturing payment.
                    return redirect(usershop)
            else:

                # if signature verification fails.
                return render(request, 'userpages/paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()
    

def order_return(request, id):
    order = OrderProduct.objects.get(id=id)
    quantitys = SizeVariant.objects.get(uid=order.sizevariant.uid)
    acc = CustomUser.objects.get(email=request.user)
    if acc.wallet is None:
        acc.wallet = 0
    acc.wallet += order.price
    acc.save()
    order.status = "Returned"
    order.save()
    quantitys.Stock += order.quantity
    quantitys.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def wishlist_to_cart(request ,cart_id):
    thiscartitem = CartItem.objects.get(id = cart_id)
    slug = thiscartitem.product.slug
    if not thiscartitem.sizemodel:
        messages.warning(request, 'Confirm your Size Variant.')
        thiscartitem.delete()
        url = reverse(get_product, args=[slug])
        return redirect(url)
    thiscartitem.is_active = True
    thiscartitem.save()
    return redirect(wishlist)



#hello text from git
