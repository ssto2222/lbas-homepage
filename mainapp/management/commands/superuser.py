from django.core.management.base import BaseCommand
from mainapp.models.account_models import UserManager
#from django.contrib.auth import get_user_model
from django.conf import settings
from mainapp.models.user_models import User

#User = get_user_model()

# 

from django.contrib.auth.management.commands import createsuperuser
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Automatically creates a superuser'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(email=settings.SUPERUSER_NAME).exists():
            email = settings.SUPERUSER_EMAIL
            password = settings.SUPERUSER_PASSWORD

            # createsuperuserコマンドを呼び出してスーパーユーザーを作成
            call_command('createsuperuser', email=email, password=password, interactive=False)

            self.stdout.write(self.style.SUCCESS('Superuser created successfully: {}'.format(email)))

# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         usermanager = UserManager()
#         if not User.objects.filter(email=settings.SUPERUSER_NAME).exists():
#             usermanager.create_superuser(
#                 email=settings.SUPERUSER_EMAIL,
#                 password=settings.SUPERUSER_PASSWORD
#             )
            
#             print("スーパーユーザー作成")

#class UserManager(BaseUserManager):
#     def create_user(self,email,password=None):
#         if not email:
#             raise ValueError('Users must have an email address')
#         user = self.model(
#             email=self.normalize_email(email),
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self,email,password=None):
#         user = self.create_user(
#             email,
#             password=password
#         )
#         user.is_admin = True
#         user.is_active = True
#         user.save(using=self._db)
#         return user