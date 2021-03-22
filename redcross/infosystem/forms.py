from django import forms
from django.contrib.auth.models import User
from .models import DonateMoney, DonateResources, ReceiveMoney, ReceiveResources


# 用户登录注册时字段
class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'用户名'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg','placeholder':'密码'}))
    
    class Meta:
        model = User
        fields = ['username', 'password']


# 查询字段
class DonateMoneyForm(forms.ModelForm):
    class Meta:
        model = DonateMoney
        fields = ('id', 'org_name', 'province', 'date', 'quantity', 'receipt_id', 'intention') 

     
class DonateResourcesForm(forms.ModelForm):
    class Meta:
        model = DonateResources
        fields = ('id', 'org_name', 'res_name', 'province', 'date', 'size', 'unit', 'quantity', 'receipt_id', 'intention') 

     
class ReceiveMoneyForm(forms.ModelForm):
    class Meta:
        model = ReceiveMoney
        fields = ('id', 'rec_name', 'province', 'date', 'quantity') 
 
        
class ReceiveResourcesForm(forms.ModelForm):
    class Meta:
        model = ReceiveResources
        fields = ('id', 'rec_name', 'res_name', 'province', 'date', 'size', 'unit', 'quantity') 
     