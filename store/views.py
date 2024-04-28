from django.shortcuts import get_object_or_404, render
from config import settings
from .models import  Category, Product

def categories(req):
    return {
        'categories': Category.objects.all()
    }
    
def category_list(req, category_slug):
    category = get_object_or_404(Category,slug=category_slug)
    products = Product.objects.filter(category=category)
    
    context = {'category': category, 
               'products':products}
    return render(req,'store/products/category.html',context)

def product_all(req):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products,'categories':categories}
    return render(req, 'store/home.html', context)

def stripe(req):
    #pricing_table_id = "prctbl_1P8II3HVLrKePmGrwhnUz6hK" #live
    STRIPE_SECRET_KEY = "sk_test_51P7vi4HVLrKePmGr3Is1klGao7eVOxBwP4zQYRF36XHsHmueHVRHxDbvofKlGpUu6fr0NTLvUHjBfvM3bkEXW2NF00AbkIWfhS"
    pricing_table_id = "prctbl_1P8H8yHVLrKePmGrBQIbXfll" #test
    context = {
        "published_key":"pk_test_51P7vi4HVLrKePmGrQSNhfZYtIMes8WpbUWOQ9NJxGcJRshUECb1RfyaWc1wgzpyIOxcgbng631trUKRdojyWC0cj00zvXi9Lnw",
        "pricing_table_id" : pricing_table_id,
               }
    return render(req, 'store/stripe.html', context)

def paypay(req):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products,'categories':categories}
    return render(req, 'store/paypay.html', context)

def product_single(req,slug):
    product = get_object_or_404(Product,slug=slug, in_stock=True)
    context = {'product': product}
    return render(req,'store/products/single.html',context)
