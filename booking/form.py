from django import forms

class BookingForm(forms.Form):
    username = forms.CharField(max_length=100, label='お名前',required=True)
    line_id = forms.CharField(max_length=100, label='LINE ID',required=False)
    remarks = forms.CharField(label='備考', widget=forms.Textarea(), required=False)
