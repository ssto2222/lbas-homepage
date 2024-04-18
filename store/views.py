from django.shortcuts import get_object_or_404, render

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

def product_single(req,slug):
    product = get_object_or_404(Product,slug=slug, in_stock=True)
    context = {'product': product}
    return render(req,'store/products/single.html',context)
