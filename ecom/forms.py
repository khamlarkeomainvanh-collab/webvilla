from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Feedback
from .models import Orders


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password']
        widgets = {'password': forms.PasswordInput()}
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile','profile_pic']

class ProductForm(forms.ModelForm):
    class Meta:
        model=models.Product
        fields=['category','name','price','description','product_image','is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

#address of shipment
# ແກ້ໄຂບ່ອນນີ້ໃນໄຟລ໌ forms.py
class AddressForm(forms.Form):
    Mobile  = forms.CharField(max_length=20)
    Address = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3}))

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['name','feedback']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['status']

    widgets = {
        'status': forms.Select(attrs={'class': 'form-control'})
    }

#for contact us page
class ContactusForm(forms.ModelForm): # ຕ້ອງເປັນ ModelForm ເທົ່ານັ້ນ ຈຶ່ງຈະມີຄຳສັ່ງ .save()
    class Meta:
        model = Feedback
        fields = ['name', 'feedback']
        labels = {
            'name': 'ຊື່ຂອງທ່ານ',
            'feedback': 'ຄຳຕິຊົມ/ຂໍ້ຄວາມ',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ກະລຸນາໃສ່ຊື່ຂອງທ່ານ', 'class': 'form-control'}),
            'feedback': forms.Textarea(attrs={'placeholder': 'ຂຽນຄຳຕິຊົມຂອງທ່ານຢູ່ນີ້...', 'class': 'form-control', 'rows': 4}),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model  = models.Expense
        fields = ['date', 'category', 'description', 'amount']
        labels = {
            'date':        'ວັນທີ',
            'category':    'ໝວດໝູ່',
            'description': 'ລາຍລະອຽດ',
            'amount':      'ຈຳນວນ (ກີບ)',
        }
        widgets = {
            'date':        forms.DateInput(attrs={'type': 'date'}),
            'category':    forms.TextInput(attrs={'placeholder': 'ໝວດໝູ່'}),
            'description': forms.TextInput(attrs={'placeholder': 'ລາຍລະອຽດ (ຖ້າມີ)'}),
            'amount':      forms.NumberInput(attrs={'placeholder': '0', 'min': '0'}),
        }