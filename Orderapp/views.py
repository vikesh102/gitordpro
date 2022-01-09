
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from Orderapp.models import Product
from .cart import Cart



def index(request):
	return render (request, 'Orderapp/products.html')

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    products = []
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        products.append(item)
    context = { 'cart': cart }
    context['products'] = products
    return render(request, 'cart/detail.html', context)


