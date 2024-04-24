from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from store.models import Product
from .basket import Basket
import json
import datetime

def basket_summary(req):
    context = {'basket':Basket(req)}
    return render(req, 'store/basket/summary.html',context)

def basket_add(req):
    basket = Basket(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('productid'))
      
        qty = int(req.POST.get('productqty'))
        date = req.POST.get('date')
        product = Product.objects.get(id=product_id)
        
        is_added = basket.add(product=product, qty=qty, date=date)
        if is_added:
            msg = 'カートに商品を追加しました。'
        else:
            msg = '同じ商品がすでに追加されています。'
       
        context ={'qty':basket.__len__(), 
                  'message':msg,
                  'is_added':is_added}
        # basketqty=basket.__len__()
        return JsonResponse((context))
    
def basket_delete(req):
    
    basket = Basket(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('productid'))
        basket.delete(product=product_id)
        
        context = {'qty':basket.__len__(),
                   'subtotal':basket.get_total_price()
                }
        return JsonResponse((context))
    
def basket_update(req):
    basket = Basket(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('productid'))
        qty = int(req.POST.get('productqty'))
        date = req.POST.get('date')
        basket.update(product=product_id, qty=qty,date=date)
        context = {'qty':basket.__len__(),
                   'subtotal':basket.get_total_price(),
                   'message':'製品の数量または納期が変更されました。'
                }
        return JsonResponse((context))