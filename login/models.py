
# from django.db import models
# from django.contrib.auth.models import User
# import uuid
# from django.contrib.auth.models import AbstractUser
# # Create your models here.
# class Profile(models.Model):
#     user=models.OneToOneField(User,   on_delete=models.CASCADE,related_name="profile")
#     phone_number=models.CharField(max_length=15)
#     otp=models.CharField(max_length=100,null=True,blank=True)
#     uid=models.CharField(default=f'{uuid.uuid4}',max_length=200)


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_email_otp

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,null=True,blank=True)
    phone_number = models.CharField(max_length=12,unique=True,null=True,blank=True)
    otp=models.CharField(max_length=100,null=True,blank=True)
    uid=models.CharField(default=f'{uuid.uuid4}',max_length=200)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    wallet = models.FloatField(null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    




# @receiver(post_save , sender = CustomUser)
# def  send_email_token(sender , instance , created , **kwargs):
#     try:
#         if created:
#             email_token = str(uuid.uuid4())
#             CustomUser.objects.create(user = instance , email_token = email_token)
#             email = instance.email
#             send_email_otp(email , email_token)

#     except Exception as e:
#         print(e)
