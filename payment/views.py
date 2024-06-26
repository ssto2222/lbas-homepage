from django.shortcuts import render,redirect,get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse,HttpResponse
from mainapp.models.user_models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.generic import View
from django.views.generic.base import TemplateView
#from orders.views import payment_confirmation
from store.models import Product
from mainapp.models.profile_models import Profile
from orders.models import Order
from basket.basket import Basket
import os,json
import stripe
import paypayopa

def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/checkout_complete.html')


class Error(TemplateView):
    template_name = 'payment/error.html'

@login_required
def basket_view(request): 
    
    context={}
    return render(request,'payment/checkout_form.html',context)

    
@require_POST
@login_required
def create_stripe_payment(request):
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    basket = Basket(request)
    total = int(basket.get_total_price())
    discount = []
    if request.POST.get('paytype') == 'default':
        amount = int(total * 0.9)
        amount_text = '¥{:,}'.format(amount)
        discount_plan = {'type':'月払い 10%割引','price':'-{:,}'.format(int(total * 0.1))}
        discount.append(discount_plan)
    elif request.POST.get('paytype')=='pre':
        amount = int(total * 0.7)
        amount_text = '¥{:,}'.format(amount)
        discount_plan = {'type':'一括前払い特典　30%割引','price':'-{:,}'.format(int(total * 0.3))}
        discount.append(discount_plan)
    try:
       
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='jpy',
            metadata={
                'userid':request.user.id,
            },
            automatic_payment_methods={
                'enabled': True,
                "allow_redirects": "never"
            },
            
        )
        
        context={'client_secret':payment_intent.client_secret,
                 'amount':amount,
                 'amount_text':amount_text,
                 'discount':discount,
                 'payment_intent_id':payment_intent.id,
                 'payment_method_id':payment_intent.payment_method,
                 'STRIPE_PUBLISHED_KEY':os.environ['STRIPE_PUBLISHED_KEY'],
                 'customer_email':request.user.email,
                 'payment_type':request.POST.get('paytype'),
                 }
        return render(request,'payment/checkout_form.html',context)
    except Exception as e:
        return JsonResponse(error=str(e))

@login_required
def stripe_confirm(request):
    context={}
    context['email']=request.user.email
    return render(request, 'payment/checkout_complete.html',context)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


@login_required
def upgrade(request):
    
    context={}
    return render(request,'payment/upgrade.html',context)

@login_required
def payment_method(request):
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    basket = Basket(request)
    total = int(basket.get_total_price())
    payment_method ='card'
    context = {}
    payment_intent = stripe.PaymentIntent.create(
        amount = total,
        currency='jpy',
        payment_method_types = ['card']
    )
    
    if payment_method == 'card':
        context['client_secret'] = payment_intent.client_secret
        context['payment_intent_id'] = payment_intent.id
        context['STRIPE_PUBLISHED_KEY'] = os.environ['STRIPE_PUBLISHED_KEY']
        context['stripe_plan_id']=os.environ['STRIPE_PRODUCT_ID']
        context['customer_email']=request.user.email
        return render(request, 'payment/card.html',context)

@require_POST
@login_required
def payment_method1(request):
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    plan = request.POST.get('plan', 'd')
    payment_method = request.POST.get('payment_method','card')
    amount = request.POST.get('amount')
    print(amount)
    context = {}
    payment_intent = stripe.PaymentIntent.create(
        amount = amount,
        currency='jpy',
        payment_method_types = ['card']
    )
    
    if payment_method == 'card':
        context['client_secret'] = payment_intent.client_secret
        context['payment_intent_id'] = payment_intent.id
        context['STRIPE_PUBLISHED_KEY'] = os.environ['STRIPE_PUBLISHED_KEY']
        context['stripe_plan_id']=os.environ['STRIPE_PRODUCT_ID']
        context['customer_email']=request.user.email
        return render(request, 'payment/card.html',context)
    
@login_required
def card(request):
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    payment_intent_id = request.POST['payment_intent_id']
    payment_method_id = request.POST['payment_method_id']
    stripe_plan_id = request.POST['stripe_plan_id']
    automatic = 'on'
    if automatic == 'on':
       customer = stripe.Customer.create(
           email = request.user.email,
           payment_method=payment_method_id,
           invoice_settings={
               'default_payment_method': payment_method_id
           }
       )
       
       stripe.Subscription.create(
           customer=customer.id,
           items=[
               {  
                   'plan': stripe_plan_id
               }
           ]
       )
    else:
        stripe.PaymentIntent.modify(
            payment_intent_id,
            payment_method=payment_method_id
        )
    
    stripe.PaymentIntent.confirm(
       payment_intent_id
    )
    context={}
    return render(request,'payment/thankyou.html',context)

@login_required
def checkout_complete(request):
    context={}
    return render(request,'payment/thankyou.html',context)

def purchase_paypay(req, product_slug):
    product = get_object_or_404(Product,slug=product_slug)
    client = paypayopa.Client(auth=(API_KEY, API_SECRET), production_mode=False)
    client.set_assume_merchant("MERCHANT_ID")
    
    context = { 
               'product':product
               }
    return render(req,'payment/checkout_paypay.html',context) 


@login_required
def checkout_paypay(request,product_slug):
    product = Product.objects.get(slug=product_slug)
        
    context={ 'product':product,
                'amount':product.price,
                'amount_text':str(product.price),
                'customer_email':request.user.email,
                }
    return render(request,'payment/checkout_paypay.html',context)


@login_required
def checkout_paypay_complete(request):
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        fullname = request.POST.get('fullname')
        add1 = request.POST.get('add1')
        add2 = request.POST.get('add2')
        postcode = request.POST.get('postcode')
        ordertotal = request.POST.get('amount')
        
        profile = Profile.objects.get(user=request.user)
        
        
        #Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            Order.objects.create(user_id=user_id,
                                         #deadline=datetime(date),
                                        full_name=fullname, 
                                        address1=add1,
                                        address2=add2, 
                                        post_code=postcode,
                                        order_total=ordertotal,
                                        order_key=order_key)

        response = JsonResponse({'success': 'Adding oder to the list succeeded'})
       
        return response
    
        
    context={ 
                }
    return render(request,'payment/paypay.html',context)
   