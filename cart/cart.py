from decimal import Decimal
from django.conf import settings
from SklepInternetowy.models import Product

class Cart(object):

    def __init__(self, request):
        #inicjalizacja koszyka
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #brak koszyka -> zapisz pusty w sesji
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart