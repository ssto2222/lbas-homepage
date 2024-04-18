from django import forms
from django.contrib.auth.forms import (PasswordResetForm,SetPasswordForm)
from django.contrib.auth import get_user_model
from .models.profile_models import Profile
from .models.user_models import User

class UserCreationForm(forms.ModelForm):
    password = forms.CharField()
    
    class Meta:
        model = get_user_model()
        fields = ('email',)
        
    def clean_password(self):
        password =self.cleaned_data.get("password")
        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'username',
            'zipcode',
            'prefecture',
            'city',
            'address1',
            
            
        )
        
class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = User.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'そのE-mailアドレスは登録されていません。')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='新しいパスワード', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='もう一度入力してください。', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))
        