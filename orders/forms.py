from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        labels = {
                    'first_name': 'Imię',
                    'last_name': 'Nazwisko',
                    'email': 'E-mail',
                    'address': 'Adres',
                    'postal_code': 'Kod pocztowy',
                    'city': 'Miasto',
        }