from django.core.management.base import BaseCommand
#from django.contrib.auth import get_user_model
from django.conf import settings
from mainapp.models.user_models import User

#User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username=settings.SUPERUSER_NAME).exists():
            User.objects.create_superuser(
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD
            )
            print("スーパーユーザー作成")