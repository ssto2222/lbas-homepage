from django.shortcuts import render,redirect
from blog.models import Article
from booking.models import Booking
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.http import  HttpResponse, JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .tokens import account_activation_token
from .models.user_models import User
from .models.profile_models import Profile
from mainapp.forms import UserCreationForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,logout
from django.core.mail import send_mail
from config import settings
from datetime import datetime, date, timedelta, time
from django.db.models import Q
from django.utils.timezone import localtime, make_aware
from orders.views import user_orders
from booking.form import BookingForm
from django.views.decorators.http import require_POST
import stripe
import os


def index(request):
    objs=Article.objects.all()
    context={
        'articles': objs
    }
    return render(request,'mainapp/index.html',context)

def signup(request):
    context={}
    print(request)
    # if request.user.is_authenticated:
    #     return redirect('/')
    if request.method == 'POST':
        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            login(request,user)
            messages.success(request,"登録完了！")
            current_site = get_current_site(request)
            subject = 'LBASアカウントをアクティベートしてください'
            message = render_to_string('mainapp/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            print(message)
            user.email_user(subject=subject, message=message)
            my_text = '新規登録が成功しました。\nアクティベーション用のリンクをご登録メールにお送りしました。\
                \n（迷惑メールフォルダに入っている可能性があります。）\
                \nregistered succesfully and activation sent'
            print("request post is ok")
            return HttpResponse(my_text.encode('Shift_JIS'),content_type='text/plain')
        else:
            context = {'form':form}
    return render(request,'mainapp/auth.html',context)

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        print('uid, userが見つかりません。')
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        login(request,user)
        return redirect('/')
    else:
        return render(request,'mainapp/registration/activation_invalid.html')
    
      
    

class Login(LoginView):
    template_name = 'mainapp/auth.html'

    def form_valid(self,form):
        messages.success(self.request, "ログイン完了！")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "ログイン失敗！")
        return super().form_invalid(form)

def logout(request):
    context={}
    return render(request,'mainapp/logout.html',context)

@login_required
def dashboard(request):
    context={}
    try:
        orders = user_orders(request)['orders']
        #preorders = user_orders(request)['preorders']
        #context['orders']=orders
        #context['preorders']=preorders
    except:
        print('no orders')
    
    is_admin = False
    user = User.objects.get(email=request.user.email)
    if user.is_admin == True:
        is_admin = True
    
    context = { 'is_admin': is_admin}
   
    return render(request,'mainapp/dashboard.html',context)

@login_required
def account(request):
    print(request.user)
    profile=Profile.objects.get(user=request.user)
    
    
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        print(form)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request,"アカウント情報更新完了！")
            context={'profile':profile}
            return render(request,'mainapp/account.html',context)
    context={'profile':profile}
    return render(request,'mainapp/account.html',context)

@login_required
def account_update(request):
   
    print("username",request.POST.get('username'))
    user=User.objects.get(id=request.POST.get('key'))
    
    defaults={
            'username':request.POST.get('username'),
            'prefecture':request.POST.get('prefecture'),
            'city':request.POST.get('city'),
            'address1':request.POST.get('address1'),
            'address2':request.POST.get('address2'),
            'zipcode':request.POST.get('zipcode')}
    try:
        obj = Profile.objects.get(user=user)
      
        for key, value in defaults.items():
            setattr(obj, key, value)
        obj.user = user
        obj.save()
    except Profile.DoesNotExist:
        new_values = {'user': user}
        new_values.update(defaults)
        obj = Profile(**new_values)
        obj.save()
    context = {'msg':'アカウント更新完了！','profile':defaults}
    return JsonResponse((context))
    # if created:
    #     messages.success(request,"アカウント情報更新完了！")
    #     context={'message':'更新完了', 'profile':profile}
    #     return JsonResponse((context))
    

@login_required
def delete_user(request):
    context={'email':request.user.email}
    if request.method == 'POST':
        redirect_url = reverse('mainapp:delete_confirmation')
        email=request.user.email
        
        params=urlencode({'email':email})
        url=f'{redirect_url}?{params}'
        return redirect(url)
    return render(request,'mainapp/user/delete_confirmation.html',context)

@login_required
def delete_confirmation(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        print(email)
        user = User.objects.get(email=email)
        if user is not None:
            
            user.is_active=False
            user.delete()
            logout(request)
            
            my_text = f'{email}様のアカウントは削除されました。\nご利用いただきありがとうございました。'
            return HttpResponse(my_text.encode('Shift_JIS'),content_type='text/plain')
    
    

def delete_cancel(request):
    email = request.GET.get('email')
    return redirect('/account')

def contact(request):
    context = {}
    if request.method == 'POST':
        print("contact posted")
        subject = request.POST.get('subject')
        message = "お問い合わせがありました。\n名前: {}\nメールアドレス: {}\n内容: {}".format(
                    request.POST.get('name'),
                    request.POST.get('email'),
                    request.POST.get('content'))        
        
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [
        settings.DEFAULT_FROM_EMAIL, 
        ]
        print("{}, {} ".format(email_from,settings.EMAIL_HOST_PASSWORD))
        
        send_mail(subject,
                  message, 
                  email_from,
                  email_to,
                  fail_silently=True,
                  )
        messages.success(request,'お問い合わせいただきありがとうございました。ご入力内容が送信されました。')
    return render(request,'mainapp/contact.html',context)


def privacy(request):
    context={}
    return render(request, 'mainapp/privacy.html',context)

def com_transaction(request):
    context={}
    return render(request, 'mainapp/marchant_law.html',context)

@csrf_exempt
def quotation(request):
    context={}
    return render(request,'mainapp/quotation.html',context)

def success(request):
    user = User.objects.get(id=request.user.id)
    context={"username": user.email}
    return render(request,'mainapp/success.html',context)

def cancel(request):
    context={}
    return render(request,'mainapp/cancel.html',context)



from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError

@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)


class CalendarView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_staff:
            start_date = date.today()
            weekday = start_date.weekday()
            if weekday != 6:
                start_date = start_date - timedelta(days=weekday + 1)
            return redirect('mainapp:schedule',start_date.year,start_date.month,start_date.day)
        # user = User.objects.get(id=request.user.id)
        today=date.today()
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            start_date = date(year=year,month=month,day=day)
        else:
            start_date = today
        days = [start_date + timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]
        
        calendar = {}
        for hour in range(10,15):
            row ={}
            
            for day in days:
                if day.weekday() == 2 or day.weekday() == 4:
                    row[day] = True
                else:
                    row[day] = False
            calendar[hour] = row
        for hour in range(19,22):
            row ={}
            
            for day in days:
                if day.weekday() == 0 or  day.weekday() == 4 or  day.weekday() == 5:
                    row[day] = False
                else:
                    row[day] = True
            calendar[hour] = row
        # start_time = make_aware(datetime.combine(start_day, time(hour=10,minute=0,second=0)))
        # end_time = make_aware(datetime.combine(end_day, time(hour=20,minute=0,second=0)))
        #booking_data = Booking.objects.exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        booking_data = Booking.objects.all()
        for booking in booking_data:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] = False
        user_book = Booking.objects.filter(email=request.user)
        context={
            'user_book':user_book,
            'calendar': calendar,
            'today':today,
            'days': days,
            'start_day' : start_day,
            'end_day' : end_day,
            'before' : days[0] -timedelta(days=7),
            'next' : days[-1]  + timedelta(days=1),    
        } 
               
        return render(request,'mainapp/calendar.html', context) 
    
class  BookingView(View):
    def get(self,request,*args,**kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        form = BookingForm(request.POST or None)
        
        context = {
            "year":year,
            "month":month,
            "day":day,
            "hour":hour,
            "form":form
        }
        
        return render(request,'mainapp/booking.html',context)
    
    def post(self,request,*args,**kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        start = datetime(year=year,month=month,day=day,hour=hour)
        end = datetime(year=year,month=month,day=day,hour=hour+1)
        start_time = make_aware(start)
        end_time = make_aware(end)
        booking_data = Booking.objects.filter(start=start_time)
        form = BookingForm(request.POST or None)
        if booking_data.exists():
            form.add_error(None, 'すでに予約があります。\n 別の日時で予約をお願いします。')
        else:
            if form.is_valid():
                booking = Booking()
                booking.start = start_time
                booking.end = end_time
                booking.name = form.cleaned_data['username']
                booking.email= request.user
                booking.line_id = form.cleaned_data['line_id']
                booking.remarks = form.cleaned_data['remarks']
                booking.save()
                mail_start = "{}/{}/{} {}時".format(year,month,day,hour)
                mail_end = "{}時".format(hour+1)
                subject = "LBASレッスン{}~{}の予約完了".format(mail_start,mail_end)
                message = "{}様、ご予約ありがとうございます。\n日時: {}~{}\n備考: {}".format(
                    form.cleaned_data['username'],
                    mail_start,
                    mail_end,
                    request.POST.get('remarks')) 
                mail_to_customer(request,subject,message)
                messages.success(request,"予約完了しました。メールをご確認ください。")
                return redirect('/')
        
        context = {
            
            "year":year,
            "month":month,
            "day":day,
            "hour":hour,
            "form":form
        }
        return render(request, 'mainapp/booking.html', context)
    
class ScheduleView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        today = date.today()
        if year and month and day:
            start_date = date(year=year,month=month,day=day)
        else:
            start_date = today
        days = [start_date + timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]
        
        calendar = {}
        for hour in range(10,15):
            row ={}
            
            for day in days:
               
                if day.weekday() == 2 or day.weekday() == 4:
                    row[day] = ""
                else:
                    row[day] = "休み(主)"
            calendar[hour] = row
        for hour in range(19,22):
            row ={}
            
            for day in days:
               
                if day.weekday() == 0 or  day.weekday() == 4 or  day.weekday() == 5:
                    row[day] = "休み(主)"
                else:
                    row[day] = ""
            calendar[hour] = row
        # start_time = make_aware(datetime.combine(start_day, time(hour=10,minute=0,second=0)))
        # end_time = make_aware(datetime.combine(end_day, time(hour=20,minute=0,second=0)))
        booking_data = Booking.objects.all()
        for booking in booking_data:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] = booking.name
        
        context={
            'user':user,
            'booking_data':booking_data,
            'calendar': calendar,
            'days': days,
            'start_day' : start_day,
            'end_day' : end_day,
            'before' : days[0] -timedelta(days=7),
            'next' : days[-1]  + timedelta(days=1), 
            'year':year,
            'month': month,
            'day': day,   
        } 
               
        return render(request,'mainapp/schedule.html', context) 

@require_POST
def holiday(request,year,month,day,hour):
    user = request.user
    if user.is_staff:
        start_time = make_aware(datetime(year=year,month=month,day=day,hour=hour))
        end_time = make_aware(datetime(year=year,month=month,day=day,hour=hour+1))
    
        
        Booking.objects.create(
            name = "休み",
            start = start_time,
            end = end_time,
        )
    
        start_date = date(year=year,month=month,day=day)
        weekday = start_date.weekday()
        if weekday != 6:
            start_date = start_date - timedelta(days=weekday + 1)
        return redirect('mainapp:schedule',year=start_date.year,month=start_date.month,day=start_date.day)

@require_POST
def delete(request,year,month,day,hour):
    start_time = make_aware(datetime(year=year,month=month,day=day,hour=hour))
    booking_data = Booking.objects.filter(start=start_time)
    
    booking_data.delete()
    start_date = date(year=year,month=month,day=day)
    weekday = start_date.weekday()
    
    if weekday != 6:
        start_date = start_date - timedelta(days = weekday +1)
    return redirect('mainapp:schedule',year=start_date.year,month=start_date.month,day=start_date.day) 

def user_schedule(request):
    booking_data = Booking.objects.filter(email=request.user)
    context = {
        'booking_data':booking_data,
    }
    return render(request,'mainapp/user_schedule.html',context)

@require_POST
def user_schedule_delete(request,*args,**kwargs):
    booking_id = kwargs.get('pk')
    booking_data = Booking.objects.get(id=booking_id)
    
    start = localtime(booking_data.start)
    # booking_date = local_time.date()
    # booking_hour = local_time.hour
    remarks = booking_data.remarks
    
    booking_data.delete()
    
    subject = "予約が取り消されました。"
    message = "{}様の予約が取り消されました。\n日時: {}\n備考: {}".format(
                    request.user,
                    start,
                    remarks) 
    mail_to_customer(request,subject,message)
    
    return redirect('mainapp:user_schedule') 

#顧客の購入リストを表示
@login_required
def registration(req):
    stripe.api_key = "sk_test_51P7vi4HVLrKePmGr3Is1klGao7eVOxBwP4zQYRF36XHsHmueHVRHxDbvofKlGpUu6fr0NTLvUHjBfvM3bkEXW2NF00AbkIWfhS"
    try:
        transactions = stripe.Charge.list()
      
        #transaction_data = transactions.data
    except:
        print("no transactions")
    transaction_list = []
    
    count=0
    print(transactions.data)
    for transaction in transactions.data:
        
        transactions_data = {}
        try:
            count+=1
            if transaction.customer == None:
                customer_id = ""
            else:
                customer_id = transaction.customer
            email = transaction.billing_details.email
            purchase_date=datetime.fromtimestamp(transaction.created)
            item = transaction.amount
            transactions_data["email"] = email
            transactions_data["customer_id"] = customer_id
            transactions_data["purchase_date"] = purchase_date
            transactions_data["item"]=item
            transaction_list.append(transactions_data) 
            print(email)
            
        except:
            print("No billing details")
            
    print(transaction_list)   
    
    print(count)
    context = {
          "transactions":transaction_list
        }
   
    return render(req, 'mainapp/registration.html',context)

def mail_to_customer(request,subject,message):     
    
    email_from = settings.DEFAULT_FROM_EMAIL
    email_to = [
    settings.DEFAULT_FROM_EMAIL, 
    request.user,
    ]
    print("{}, {} ".format(email_from,settings.EMAIL_HOST_PASSWORD))
    
    send_mail(subject,
                message, 
                email_from,
                email_to,
                fail_silently=True,
                )
    
    