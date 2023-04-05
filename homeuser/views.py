from django.shortcuts import render , redirect , HttpResponse
from products.models import Product ,Category ,SizeVariant
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.views.decorators.cache import cache_control

# Create your views here.

def home1(request):
    return render(request, 'product.html')


def cart(request):
    return render(request,'cart.html')

def userheader(request):
    return render(request,'userheader.html')





def userhome(request):
    if request.user.is_authenticated:
        category = Category.objects.all()
        context = {'login':'login', 'homeactive':'active' ,'category': category}
        return render(request,'userpages/userhome.html', context)
    category = Category.objects.all()
    context = {'homeactive':'active','category': category}
    return render(request,'userpages/userhome.html' ,context)




def usershop(request):
    if request.user.is_authenticated:
        category = Category.objects.all()
        product = Product.objects.order_by('product_name')
        sizevar = list(SizeVariant.objects.order_by('size_name').values_list('size_name', flat=True).distinct())
        context = {'products' :product ,'category': category ,'login':'login', 'shopactive':'active', 'sizevar':sizevar}
        return render(request, 'userpages/usershop.html' ,context)
    category = Category.objects.all()
    product = Product.objects.order_by('product_name')
    sizevar = list(SizeVariant.objects.order_by('size_name').values_list('size_name', flat=True).distinct())
    context = {'products' :product ,'category': category , 'shopactive':'active' , 'sizevar':sizevar}
    return render(request, 'userpages/usershop.html' ,context)



# def filter_products(request):
#     categories = request.GET.getlist('category')
#     sizes = request.GET.getlist('size')
#     min_price = request.GET.get('min_price', None)
#     max_price = request.GET.get('max_price', None)

#     products = Product.objects.all()
#     categorie = Category.objects.filter(slug__in = categories)


#     if categories:
#         products = products.filter(category__in=categorie)
#     # products.annotate(image = )
#     # for item in products:
#     #     for image in item.images:
#     #         print(image.image)
#     # if sizes:
#     #     products = products.filter(size__in=sizes)

#     # if min_price:
#     #     products = products.filter(price__gte=min_price)

#     # if max_price:
#     #     products = products.filter(price__lte=max_price)
#     # for item in products:
#     #     print(item.product_images.first.ima)
#     # product_images = products.product_images.all()
#     data = {
#         'products': list(products.values())
#     }
#     # print( list(products.values()))
#     # for image in product_images:
#     #     print(image.image.url)
#     return JsonResponse(data)

# def category_carousel(request):
#     categories = Category.objects.all()
#     products_by_category = {}
#     for category in categories:
#         products_by_category[category.id] = Product.objects.filter(category=category)
#     context = {'categories': categories, 'products_by_category': products_by_category}
#     return render(request, 'category_carousel.html', context)


def get_category(request , slug):
    
    try:
        singlecategory = Category.objects.get(slug =slug)
        category = Category.objects.all()
        product = Product.objects.filter(category = singlecategory)
        sizevar = list(SizeVariant.objects.order_by('size_name').values_list('size_name', flat=True).distinct())
        context = {'products' :product ,'category': category ,'login':'login', 'shopactive':'active', 'sizevar':sizevar , 'singlecategory' : singlecategory}
        return render(request, 'userpages/usershop.html' ,context)
    except Exception as e:
        print(e)
        
#logger.error

def filter_products(request):
    category = Category.objects.all()
    sizevar = list(SizeVariant.objects.order_by('size_name').values_list('size_name', flat=True).distinct())
    if request.user.is_authenticated:
        login = True
    else:login = False

    if request.method == 'POST':
        categorys = request.POST.get('category')
        size = request.POST.get('sizes')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')

        products = Product.objects.order_by('product_name')

        if categorys:
            products = products.filter(category__category_name__iexact=categorys)

        if size:
            products = products.filter(product_sizes__size_name__iexact=size)

        if min_price:
            products = products.filter(price__gte=min_price)

        if max_price:
            products = products.filter(price__lte=max_price)

    else:
        products = Product.objects.order_by('product_name')
        category = None
        size = None
        min_price = None
        max_price = None

    context = {
        'category': category,
        'sizevar': sizevar,
        'products': products,
        'categorys': categorys,
        'size': size,
        'min_price': min_price,
        'max_price': max_price,
        'filter':True,
        'login':login
    }

    return render(request, 'userpages/usershop.html', context)






def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_to_admin",
        {
            'type': 'send_notification',
            'message': json.dumps("Order recieved from sabeeh")
        }
    )
    return HttpResponse("Done")