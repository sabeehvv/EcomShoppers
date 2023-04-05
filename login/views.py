from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login ,logout
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
from .models import CustomUser
from django.core.cache import cache
from cart.views import _cart_id
from cart.models import Cart,CartItem

import random
from .helper import MessageHandler
from django.contrib import messages
from base.emails import send_email_otp


def home(request):
    if request.COOKIES.get('verified') and request.COOKIES.get('verified')!=None:
        return HttpResponse(" verified.")
    else:
        return HttpResponse(" Not verified.")


# def register1(request):
#     if request.method=="POST":
#         if CustomUser.objects.filter(email__iexact=request.POST['user_name'] ).exists():
#             return HttpResponse("User already exists")
#         if CustomUser.objects.filter(phone_number__iexact=request.POST['phone_number'] ).exists():
#             #messages.warning(request, 'number already exists.')
#             return HttpResponse("number already exists")
#         otp=random.randint(1000,9999)
#         profile=CustomUser.objects.create(email=request.POST['user_name'],phone_number=request.POST['phone_number'],otp=f'{otp}')
#         if request.POST['methodOtp']=="methodOtpWhatsapp":
#             #messagehandler =MessageHandler(request.POST['phone_number'],otp).send_otp_via_whatsapp()
#             print('OTP is =',otp)
#         else:
#             #messagehandler =MessageHandler(request.POST['phone_number'],otp).send_otp_via_message()
#             print('OTP is =',otp)
#         red=redirect(f'otp/{profile.uid}/')
#         red.set_cookie("can_otp_enter",True,max_age=600)
#         return red  
#     return render(request, 'register.html')

def otpVerify(request,uid):   
    if request.method=="POST":
        profile=CustomUser.objects.get(uid=uid)     
        if request.COOKIES.get('can_otp_enter')!=None:
            otp = request.POST['otp']
            cached_otp = cache.get(f'otp_{profile.id}')
            if str(cached_otp) == str(otp):
                cache.delete(f'otp_{profile.id}')
                dis = {'action':'logins','singin':'true','userdone':'registration successfully completed with phone number validation',}
                messages.success(request, 'registration successfully completed with phone number validation.')
                return redirect(logins)
            return render(request,"userotp.html",{'id':uid,'invalid':'wrong otp'})
        return render(request,"userotp.html",{'id':uid,'invalid':'10 minutes Over'})      
    return render(request,"userotp.html",{'id':uid})    

# def register(request):
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         username = request.POST['username']
#         email = request.POST['email']
#         pass1 = request.POST['password']

#         user = User.objects.create_user(email=email,password=pass1,first_name = first_name )
#         user.save();
#         print('user created ')
#         return redirect('/')
    
#     else:
#         return render(request,'Register.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        # date_of_birth = request.POST['date_of_birth']
        pass1 = request.POST['password']
        pass2 = request.POST['Confirm_Password']

        if (not email):
            dis = {'email':'Please Enter Email',}
            return render(request,'userregister.html',dis)
        if (not first_name):
            dis = {'first_name':'Please Enter first_name',}
            return render(request,'userregister.html',dis)
        if (not last_name):
            dis = {'last_name':'Please Enter last Name',}
            return render(request,'userregister.html',dis)
        if (not phone_number):
            dis = {'phone_number':'Please Enter phone number',}
            return render(request,'userregister.html',dis)
        # if (not date_of_birth):
        #     dis = {'date_of_birth':'Please Enter date of birth',}
        #     return render(request,'userregister.html',dis)
        if (not pass1):
            dis = {'password':'Please Enter password',}
            return render(request,'userregister.html',dis)
            

            
        if pass1 == pass2 :
            if CustomUser.objects.filter(email=email).exists():
                dis = {'email':'Email address already taken',}
                return render(request,'userregister.html',dis)
            elif CustomUser.objects.filter(phone_number=phone_number).exists():
                dis = {'phone_number':'phone_number already exist',}
                return render(request,'userregister.html',dis)
            else:
                otp=random.randint(1000,9999)
                # send_email_otp(email , otp)
                #messagehandler =MessageHandler(request.POST['phone_number'],otp).send_otp_via_whatsapp()
                print('OTP is =',otp)
                user = CustomUser.objects.create_user(phone_number = phone_number , email=email,first_name = first_name ,last_name = last_name,password = pass1,otp=f'{otp}')
                user.save()
                cache.set(f'otp_{user.id}', otp, 600)
                red=redirect(f'otp/{user.uid}/')
                red.set_cookie("can_otp_enter",True,max_age=600)
                return red 
                # dis = {'userdone':'registration successfully completed',}
                # return render(request,'userlogin.html',dis)
        else:
            print('Password not matching')
            dis = {'password':'Password not matching',}
            return render(request,'userregister.html',dis)
    else:
        return render(request,'userregister.html')
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logins(request):
    if request.user.is_authenticated:
            context = {'login':'login'}
            return render(request,'userpages/userhome.html', context)
    if request.method == 'POST':
        email = request.POST['email']
        # password = request.POST['password']
        otp=random.randint(1000,9999)
        user = CustomUser.objects.filter(email=email).first()
        print('authenticated')
        if user is not None and not user.is_active:
            dis = {'action':'logins','invalid':'Your account is blocked, contact customer service','singin':'true'}
            return render(request,'userlogin.html',dis)

        if user is not None:
            if request.POST['loginwith']=="otpsms":
                phone_number = user.phone_number 
                print(phone_number)
                print('OTP is =',otp)
                # MessageHandler(phone_number,otp).send_otp_via_whatsapp()
                # MessageHandler(phone_number,otp).send_otp_via_message()
                send_email_otp(email , otp)
                cache.set(f'otp_{user.id}', otp, 600)
                dis = {'action':'loginsotp','otpmethode': 'true' ,'email':email,'readonly':'readonly'}
                return render(request,'userlogin.html',dis)
            elif request.POST['loginwith']=="validpassword":
                dis = {'action':'loginspass','passwordmethod':'true','email':email,'readonly':'readonly'}
                return render(request,'userlogin.html',dis)
        else:
            print('invalid user')
            dis = {'action':'logins','invalid':'invalid username','singin':'true'}
            return render(request,'userlogin.html',dis)

    else:
        dis = {'action':'logins','singin':'true'}
        return render(request,'userlogin.html',dis)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginsotp(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = request.POST['OTP']
        user = CustomUser.objects.get(email=email)
        cached_otp = cache.get(f'otp_{user.id}')
        if str(cached_otp) == str(otp):
            cache.delete(f'otp_{user.id}')
            try:
                #guestuser cart
                cart = Cart.objects.get(cart_id = _cart_id(request))
                cart_item = CartItem.objects.filter(cart = cart)
                user_cart = CartItem.objects.filter(user = user)
                
                for x in cart_item:
                    a=0
                    for y in user_cart:
                        if x.product == y.product:
                            y.quantity += x.quantity 
                            y.save()
                            x.delete()
                            a=1
                            break
                    if a==0:
                        x.user=user
                        x.save()
            except:
                pass

            print('otp varified')
            login(request, user)
            context = {'login':'login'}
            return render(request,'userpages/userhome.html', context)
        dis = {'action':'loginsotp','otpmethode':'true','invalid':'invalid OTP','email':email,'readonly':'readonly'}
        return render(request,'userlogin.html',dis)
    return render(request,'userlogin.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginspass(request):
    if request.user.is_authenticated:
            return redirect('Homeheader')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email,password=password)

        if user is not None:
            try:
                #guestuser cart
                cart = Cart.objects.get(cart_id = _cart_id(request))
                cart_item = CartItem.objects.filter(cart = cart)
                user_cart = CartItem.objects.filter(user = user)
                
                for x in cart_item:
                    a=0
                    for y in user_cart:
                        if x.product == y.product:
                            y.quantity += x.quantity 
                            y.save()
                            x.delete()
                            a=1
                            break
                    if a==0:
                        x.user=user
                        x.save()
            except:
                pass

            # Cart.objects.all().delete()
            login(request, user)
            context = {'login':'login'}
            return render(request,'userpages/userhome.html', context)
        else:
            print('invalid password')
            dis = {'action':'loginspass','passwordmethod':'true','invalid':'invalid password','email':email,'readonly':'readonly'}
            return render(request,'userlogin.html',dis)

    else:
        return render(request,'userlogin.html')

    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logouts(request):
    logout(request)
    return redirect('logins')

