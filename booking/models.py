from django.db import models
from mainapp.models.user_models import User
from django.utils import timezone

# Create your models here.
class Booking(models.Model):
    name = models.CharField('名前',max_length=100,null=True,blank=True)
    email = models.EmailField('E-mail',max_length=100,null=False,blank=False)
    line_id = models.CharField('LINE ID',max_length=100,null=True,blank=True)
    remarks = models.TextField('備考',default='',blank=True)
    start = models.DateTimeField('開始時間',default=timezone.now)
    end = models.DateTimeField('終了時間',default=timezone.now)
    
    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M')
        return f'{self.email} {start}~{end}'