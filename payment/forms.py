from django import forms
from orders.models import Order

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('user','full_name', 'address1','address2','post_code')