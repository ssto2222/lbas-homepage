from django.shortcuts import render,redirect
from blog.models import Article
from django.contrib.auth.views import LoginView
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
from django.contrib.auth import login,logout
from django.core.mail import send_mail
#from orders.views import user_orders

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
        preorders = user_orders(request)['preorders']
        context['orders']=orders
        context['preorders']=preorders
    except:
        print('no orders')
    
   
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
        subject = "お問い合わせがありました。"
        message = "お問い合わせがありました。\n名前: {}\nメールアドレス: {}\n内容: {}".format(
                    request.POST.get('name'),
                    request.POST.get('email'),
                    request.POST.get('content'))        
        
        email_from = os.environ['EMAIL_HOST_USER']
        email_to = [
        os.environ['EMAIL_HOST_USER'], 
        ]
        send_mail(subject,message, email_from,email_to)
        messages.success(request,'お問い合わせいただきありがとうございました。ご入力内容が送信されました。')
    return render(request,'mainapp/contact.html',context)


def privacy(request):
    context={}
    return render(request, 'mainapp/privacy.html',context)

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
