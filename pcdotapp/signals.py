# pcdotapp/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, Product

@receiver(user_logged_in)
def merge_carts(sender, user, request, **kwargs):
    session_cart = request.session.get('cart', {})
    if session_cart:
        for product_id, cart_item in session_cart.items():
            product = Product.objects.get(id=cart_item['product_id'])
            user_cart_item, created = Cart.objects.get_or_create(user=user, product=product)
            if created:
                user_cart_item.quantity = cart_item['quantity']
            else:
                user_cart_item.quantity += cart_item['quantity']
            user_cart_item.save()
        del request.session['cart']  # Clear session cart after merging