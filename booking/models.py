from django.db import models
from mainapp.models.user_models import User
from django.utils import timezone

# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(User, verbose_name='ユーザー',on_delete=models.CASCADE)
    first_name = models.CharField('姓',max_length=100,null=True,blank=True)
    last_name = models.CharField('名',max_length=100,null=True,blank=True)
    tel = models.CharField('電話番号',max_length=100,null=True,blank=True)
    remarks = models.TextField('備考',default='',blank=True)
    start = models.DateTimeField('開始時間',default=timezone.now)
    end = models.DateTimeField('終了時間',default=timezone.now)
    
    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M')
        return f'{self.first_name}{self.last_name} {start}~{end}'