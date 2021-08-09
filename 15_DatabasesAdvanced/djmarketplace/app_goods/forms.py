from django import forms
from . models import Order


BALANCE_INCREASE_CHOICES = [(i, str(i)) for i in range(10,1110,10)]

class BalanceIncreaseForm(forms.Form):
	quantity = forms.TypedChoiceField(choices=BALANCE_INCREASE_CHOICES, coerce=int)	