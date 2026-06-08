from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, OrderItem, CustomUser


# ---------------- Home Page with Login ----------------

def home(request):
    login_error = None

    if request.method == 'POST' and 'login' in request.POST:
        mobile = request.POST.get('login_mobile')
        password = request.POST.get('login_password')
        user = authenticate(request, mobile=mobile, password=password)
        if user is not None:
            login(request, user)
            return redirect('categories')
        else:
            login_error = "Invalid mobile number or password."

    return render(request, 'home.html', {
        'login_error': login_error
    })


# ---------------- Separate Register View ----------------

def user_register(request):
    register_error = None

    if request.method == 'POST':
        name = request.POST.get('register_name')
        mobile = request.POST.get('register_mobile')
        email = request.POST.get('register_email')
        password = request.POST.get('register_password')

        if CustomUser.objects.filter(mobile=mobile).exists():
            register_error = "Mobile number already registered."
        elif CustomUser.objects.filter(email=email).exists():
            register_error = "Email already registered."
        else:
            user = CustomUser.objects.create_user(
                username=name,
                mobile=mobile,
                email=email,
                password=password
            )
            login(request, user)
            return redirect('profile')

    return render(request, 'register.html', {
        'register_error': register_error
    })


# ---------------- Category and Product Views ----------------

def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'products': products})


# ---------------- Cart Views ----------------

def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total += product.price * quantity
        products.append({'product': product, 'quantity': quantity})
    return render(request, 'cart.html', {'cart_items': products, 'total': total})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return JsonResponse({'success': True})


def update_cart(request, product_id, action):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        if action == 'increase':
            cart[product_id] += 1
        elif action == 'decrease':
            cart[product_id] -= 1
            if cart[product_id] <= 0:
                del cart[product_id]
    request.session['cart'] = cart
    return JsonResponse({'success': True})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
    request.session['cart'] = cart
    return JsonResponse({'success': True})


# ---------------- User Authentication ----------------

def user_logout(request):
    logout(request)
    return redirect('home')


# ---------------- User Profile and Orders ----------------

@login_required
def user_profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'orders': orders})
