from django import forms
from .models import Account, Transaction
from django.forms import NumberInput, TextInput

class AccountModelForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("name",)
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
            }),
        }
    def __init__(self, *args, **kwargs):
        super(AccountModelForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class":"form-control"})

class TransactionModelForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ("to_account","amount")
        widgets = {
            'to_account': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Account number'
            }),
            'amount': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Amount'
            }),
        }
    def __init__(self, *args, **kwargs):
        super(TransactionModelForm, self).__init__(*args, **kwargs)
        self.fields["to_account"].widget.attrs.update({"class":"form-control"})
        self.fields["amount"].widget.attrs.update({"class":"form-control"})