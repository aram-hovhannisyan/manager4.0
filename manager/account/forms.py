from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

from tables.models import ItemsModel, Debt, Paymant

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_admin', 'is_employee', 'is_customer', 'is_supplier')

class ItemAddForm(forms.ModelForm):
    class Meta:
        model = ItemsModel
        fields = ('customer','supplier','productName', 'productPrice')

# class ItemAddForm(forms.ModelForm):
#     customer = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_customer=True), widget=forms.CheckboxSelectMultiple)

#     class Meta:
#         model = ItemsModel
#         fields = ('customer', 'supplier', 'productName', 'productPrice')


class PaymantForm(forms.ModelForm):
    class Meta:
        model = Paymant
        fields = ('date','money','returned', 'salary',)

class SalaryForm(forms.Form):
    customer = forms.CharField()
    date = forms.DateField()
    salary = forms.IntegerField()