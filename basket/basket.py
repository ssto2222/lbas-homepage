from store.models import Product
import datetime


class Basket():
    
    def __init__(self,request):
        
        self.session = request.session
        
        basket = self.session.get('skey')
        print(basket)
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket
        
    def add(self,product,qty,date):
        product_id = product.id
        is_added = False
        if str(product_id) not in self.basket.keys():
            self.basket[product_id] = {'price': str(product.price), 'qty':int(qty), 'date':date}
            self.save()
            is_added = True
        
        return is_added
    
    def delete(self,product):
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()
            
    def update(self,product,qty, date):
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = int(qty)
            self.basket[product_id]['date'] = date
            
            self.save()
    
    def clear(self):
        del self.session['skey']
        self.save()
        
        
    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product
        
        for item in basket.values():
            item['price'] = int(item['price'])
            item['qty'] =  int(item['qty'])
            item['total_price'] = item['price'] * item['qty']
            yield item
        
        
    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        
        return sum(item["qty"] for item in self.basket.values())
    
    def get_total_price(self):
        return sum(int(item["qty"]) * int(item['price']) for item in self.basket.values())
    
    def save(self):
        self.session.modified = True