from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate, login, logout
from login.models import CustomUser
from django.http import HttpResponseRedirect
from django.contrib import messages
from products.models import Category, Product, SizeVariant, ProductImage
from orders.models import Orders, OrderProduct
from datetime import datetime

# Create your views here.


def adminlogins(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('adminpage')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = CustomUser.objects.filter(email=email)
        if not user_obj.exists():
            messages.info(request, 'ACCOUNT NOT FOUND')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = authenticate(email=email, password=password)

        if user_obj and user_obj.is_superuser:
            login(request, user_obj)
            return redirect('adminpage')
        messages.info(request, 'This username is not superuser')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'adminpages/adminlogin.html')


def adminpage(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    return render(request, 'adminpages/adminhome.html', {'room_name': "broadcast"})


def aduser(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')

    userlist = {
        'users': CustomUser.objects.order_by('email'), 'userselect': True
    }
    return render(request, 'adminpages/adminuser.html', userlist)


def update_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        if user.is_active:
            user.is_active = False
            user.save()
            return redirect(aduser)
        else:
            user.is_active = True
            user.save()
            return redirect(aduser)
    return redirect(aduser)


def search_username(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminpage')
    search_term = request.GET['search_term']

    userlist = {
        'users': CustomUser.objects.filter(email__icontains=search_term)
    }
    return render(request, 'adminpages/adminuser.html', userlist)


def admincategory(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    context = {'categorys': Category.objects.all(), 'categoryselect': True
               }
    return render(request, 'adminpages/adminCategory.html', context)


def adminproduct(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    context = {'products': Product.objects.order_by('product_name'), 'categorys': Category.objects.all(
    ), 'SizeVariants': SizeVariant.objects.all(), 'productselect': True, 'room_name': "broadcast"}
    return render(request, 'adminpages/adminproduct.html', context)


def addcategory(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    if request.method == 'POST':
        categorys = Category(category_name=request.POST['Category_Name'])
        categorys.category_image = request.FILES['file-input']
        categorys.save()
        return redirect('admincategory')
    else:
        return redirect('admincategory')


def editcategory(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    if request.method == 'POST':
        category_slug = request.POST.get('slug')
        category_name = request.POST.get('Category_Name')
        category_image = request.FILES.get('file-input')
        categorys = Category.objects.get(slug=category_slug)
        if category_image:
            categorys.category_image = category_image
        categorys.category_name = category_name
        categorys.save()
        return redirect('admincategory')
    return redirect('admincategory')


def editproduct(request, slug):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    if request.method == 'POST':
        thisproduct = Product.objects.get(slug=slug)
        # thissizes = SizeVariant.objects.get(Product = Product.objects.get(slug=slug))
        thisproduct.product_name = request.POST['product_name']
        thisproduct.category = Category.objects.get(
            slug=request.POST['category'])
        thisproduct.product_desription = request.POST['product_desription']
        thisproduct.price = request.POST['price']
        size_name = request.POST.getlist('size-variant')
        size_prize = request.POST.getlist('size-price')
        checkimage = request.FILES.getlist('images')

        if checkimage:
            oldimages = thisproduct.product_images.all()
            oldimages.delete()
            for image in request.FILES.getlist('images'):
                thisproduct.product_images.create(image=image)
        if size_name:
            oldsizes = thisproduct.product_sizes.all()
            oldsizes.delete()
            for name, stock in zip(size_name, size_prize):
                thisproduct.product_sizes.create(size_name=name, Stock=stock)
        thisproduct.save()
        return redirect('adminproduct')

    context = {'product': Product.objects.get(slug=slug), 'categorys': Category.objects.all(
    ), 'SizeVariants': SizeVariant.objects.all(), 'productselect': True}
    return render(request, 'adminpages/editproduct.html', context)


def addproduct(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    if request.method == 'POST':
        product = Product(product_name=request.POST['product_name'])
        product.category = Category.objects.get(slug=request.POST['category'])
        product.product_desription = request.POST['product_desription']
        product.price = request.POST['price']
        product.save()
        # product.size_variant = request.POST['size_variant']
        size_name = request.POST.getlist('size-variant')
        size_prize = request.POST.getlist('size-price')
        for name, stock in zip(size_name, size_prize):
            product.product_sizes.create(size_name=name, Stock=stock)
        for image in request.FILES.getlist('images'):

            product.product_images.create(image=image)
        return redirect('adminproduct')
    context = {'products': Product.objects.all(), 'categorys': Category.objects.all(
    ), 'SizeVariants': SizeVariant.objects.all(), 'productselect': True, 'room_name': "broadcast"}
    return render(request, 'adminpages/addproduct.html', context)


def deleteproduct(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    if request.method == "POST":
        my_product = Product.objects.get(slug=request.POST['slug'])
        my_product.delete()
        return redirect(adminproduct)
    return redirect(adminproduct)


def deletecategory(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    if request.method == "POST":
        my_Category = Category.objects.get(slug=request.POST['slug'])
        my_Category.delete()
        return redirect(admincategory)
    return redirect(admincategory)


def adminorder(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    order = Orders.objects.order_by('-id')
    context = {'orderselect': True, 'order': order}
    return render(request, 'adminpages/adminorder.html', context)


def deletorder_item(request, order_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    thisorder = Orders.objects.get(id=order_id)
    thisorder.delete()
    return redirect(adminorder)


def admincategoryedit(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    return render(request, 'adminpages/admincategoryedit.html')


def orderdetailsadmin(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    orderprod = OrderProduct.objects.filter(order=id).order_by('-id')
    return render(request, 'adminpages/adminorderdetails.html', {'orderprod': orderprod})


def orderstatus(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('adminlogins')
    if request.method == "POST":
        status = request.POST.get('status')
        order = OrderProduct.objects.get(id=id)
        order.status = status
        order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def order_filter(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_dates = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_dates = datetime.strptime(end_date, '%Y-%m-%d').date()
        order = Orders.objects.filter(
            date__range=[start_dates, end_dates])
    else:
        order = Orders.objects.all()
    context = {'orderselect': True,
               'order': order,
               'start_date': start_date,
               'end_date': end_date
               }
    return render(request, 'adminpages/adminorder.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutadmin(request):
    logout(request)
    return redirect('adminpage')
