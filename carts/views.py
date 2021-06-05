from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Cart, CartItem
from store.models import Product

# Create your views here.
from django.http import HttpResponse

def _cart_id(request): # _를 붙여서 private function으로 만든다.
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # cart_id(session_id)를 가지고 cart를 가져옴
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1  # cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    
    return HttpResponse(cart_item.product)
    exit()
    return redirect('cart')






def cart(request):
    return render(request, 'store/cart.html')