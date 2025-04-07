from django import forms
from django.contrib.auth.models import User
from userapp.models import Cart,Orders

class RegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets={
            'password':forms.PasswordInput()
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']
        widgets={
            'password':forms.PasswordInput()
        }

class CartForm(forms.ModelForm):
    class Meta:
        model=Cart
        fields=['quantity']
        widgets={
            'quantity':forms.NumberInput(attrs={'class':'form-control'})

        }    

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['table_No']          