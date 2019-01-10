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

    def add(self, product, quantity=1, update_quantity= False):
        #dodanie produktu do koszyka lub aktualizacja ilości danego produktu
        product_id = str(product.id)
        if product.id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def save(self):
        #ustaw flagę modified aby zapisać sesję
        self.session.modified = True

    def __iter__(self):
        #iteracja po produktach w koszyku, pobranie ich z bazy

        product_ids = self.cart.keys()
        #pobranie obiektów produków i dodanie ich do koszyka
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        #liczenie przedmiotów w koszyku
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        #usuń koszyk z sesji
        del self.session[settings.CART_SESSION_ID]
        self.save()