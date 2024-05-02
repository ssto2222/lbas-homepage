from django.urls import path
from payment import views


app_name = 'payment'

urlpatterns = [
    path('basket_view/', views.basket_view,name='basket_view'),
    path('create_stripe_payment/', views.create_stripe_payment, name='create_stripe_payment'),
    path('stripe_confirm/', views.stripe_confirm, name='stripe_confirm'),
    
    path('upgrade/', views.upgrade, name='upgrade'),
    path('payment_method/', views.payment_method, name='payment_method'),
    path('card/', views.card, name='card'),
    
    path('create_stripe_payment/checkout_complete/', views.checkout_complete, name='checkout_complete'),
    path('order_placed/', views.order_placed, name='order_placed'),
    path('error/', views.Error.as_view(), name='error'),
    path('webhook/', views.stripe_webhook),
    path('purchase_paypay/<slug:product_slug>/', views.purchase_paypay,name='purchase_paypay'),
    path('checkout_paypay/<slug:product_slug>/', views.checkout_paypay,name='checkout_paypay'),
    path('checkout_paypay_complete/', views.checkout_paypay_complete,name='checkout_paypay_complete'),
]