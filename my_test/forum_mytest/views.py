from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ContactForm


def home(request):
    products = Product.objects.all()[:3]
    return render(request,'home.html',
                  {'products':products})


def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


def about(request):
    return render(request,'about.html')


def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'contact.html',
                          {'form':ContactForm(),
                           'success':True})
    else:
        form = ContactForm()

    return render(request,'contact.html',
                  {'form':form})
    
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size')

    cart = request.session.get('cart', {})

    key = f"{product_id}_{size}"

    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        cart[key] = {
            'product_id': product_id,
            'quantity': quantity,
            'size': size
        }

    request.session['cart'] = cart
    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for key, item in cart.items():

        # If old cart format (int quantity only)
        if isinstance(item, int):
            product = Product.objects.get(id=key)
            quantity = item
            size = "M"
        else:
            product = Product.objects.get(id=item['product_id'])
            quantity = item['quantity']
            size = item['size']

        subtotal = product.price * quantity
        total += subtotal

        items.append({
            'key': key,
            'product': product,
            'quantity': quantity,
            'size': size,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


def update_cart(request, key, action):
    cart = request.session.get('cart', {})

    if key in cart:
        if action == 'increase':
            cart[key]['quantity'] += 1
        elif action == 'decrease':
            cart[key]['quantity'] -= 1
            if cart[key]['quantity'] <= 0:
                del cart[key]

    request.session['cart'] = cart
    return redirect('cart')

def checkout_all(request):
    cart = request.session.get('cart', {})
    total = 0
    items = []

    for key, item in cart.items():
        product = Product.objects.get(id=item['product_id'])
        subtotal = product.price * item['quantity']
        total += subtotal

        items.append({
            'product': product,
            'quantity': item['quantity'],
            'size': item['size'],
            'subtotal': subtotal
        })

    # ✅ If user clicks Confirm & Pay
    if request.method == "POST":
        # Clear cart session
        request.session['cart'] = {}
        request.session.modified = True

        return render(request, 'checkout.html', {
            'success': True
        })

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })
    
def checkout(request):
    return render(request, 'checkout.html')


def remove_from_cart(request, key):
    cart = request.session.get('cart', {})
    if key in cart:
        del cart[key]
    request.session['cart'] = cart
    return redirect('cart')


def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'checkout.html', {
        'product': product,
        'quantity': 1,
        'total': product.price
    })