from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .account_models import UserManager
from django.core.mail import send_mail
import os
from django.conf import settings

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True)
    
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    def has_perm(self, prerm, obj=None):
        "Does the user have a specific permission?"
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app 'app_label'?"
        return True
    
    def email_user(self, subject, message):
        #email_from = os.environ['EMAIL_HOST_USER']
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [self.email]
        send_mail(
            subject,
            message,
            email_from,
            email_to,
            fail_silently=True,
        )
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

class Staff(models.Model):
    user = models.OneToOneField(User, verbose_name='スタッフ',on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user}'
    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_onetoone(sender, **kwargs):
    if kwargs['created']:
        from mainapp.models.profile_models import Profile
        
        Profile.objects.create(user=kwargs['instance'])