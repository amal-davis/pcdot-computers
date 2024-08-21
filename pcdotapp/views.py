from django.shortcuts import render
from .models import *
from urllib.parse import urlparse, urlunparse
from django.conf import Settings, settings
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
from django.contrib import messages
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User,auth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.utils.translation import activate
import requests
from django.views.decorators.http import require_POST


# Create your views here.




def index(request):
    product_types = ProductType.objects.all()
    desktop_images = DesktopCarouselImage.objects.all()
    mobile_images = MobileCarouselImage.objects.all()

    products_by_type = {
        product_type: {
            'all': Product.objects.filter(product_type=product_type).order_by('-created_at')[:16],
            'categories': {
                category: Product.objects.filter(product_type=product_type, category=category).order_by('-created_at')[:4]
                for category in product_type.category_set.all()
            }
        }
        for product_type in product_types
    }

    cart_count = 0
    wishlist_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    videos = Video.objects.select_related('product').order_by('-created_at')
    client_logos = ClientLogo.objects.all()
    links = Links.objects.all()

    return render(request, 'index.html', {
        'product_types': product_types,
        'products_by_type': products_by_type,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'videos': videos,
        'desktop_images': desktop_images,
        'mobile_images': mobile_images,
        'client_logos': client_logos,
        'links':links
    })

        





def set_language(request, language):
    next_url = request.GET.get('next', '/')
    
    if language not in dict(settings.LANGUAGES):
        language = settings.LANGUAGE_CODE
    
    activate(language)
    
    # Parse the URL and change the language code
    parsed_url = urlparse(next_url)
    path_parts = parsed_url.path.split('/')
    
    if path_parts[1] in dict(settings.LANGUAGES):
        path_parts[1] = language
    else:
        path_parts.insert(1, language)
    
    new_path = '/'.join(path_parts)
    new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, parsed_url.params, parsed_url.query, parsed_url.fragment))
    
    response = HttpResponseRedirect(new_url)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response


def about_us(request):
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    cart_count = 0
    wishlist_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request,'about_us.html',{'product_types':product_types,'categories':categories,'cart_count':cart_count,'wishlist_count':wishlist_count})


def warranty(request):
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    cart_count = 0
    wishlist_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request,'warranty_list.html',{'product_types':product_types,'categories':categories,'cart_count':cart_count,'wishlist_count':wishlist_count})


def products(request):
    product_list = Product.objects.all().order_by('-created_at')
    paginator = Paginator(product_list, 20)  # Show 20 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    cart_count = 0
    wishlist_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return render(request, 'products.html', {'page_obj': page_obj,'product_types':product_types,'categories':categories,'cart_count':cart_count,'wishlist_count':wishlist_count})


def product_page(request, slug):
    product = get_object_or_404(Product, slug=slug)
    recommended_products = Product.objects.filter(product_type=product.product_type).exclude(id=product.id).order_by('-created_at')[:3]
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    
    # Initialize cart_count and wishlist_count with default values
    cart_count = 0
    wishlist_count = 0
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return render(request, 'product_pages.html', {
        'product': product,
        'categories': categories,
        'recommended_products': recommended_products,
        'product_types': product_types,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    })






@login_required(login_url='signin')
def add_to_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')



@login_required(login_url='signin')
def wishlist(request):
    cart_count = 0
    wishlist_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'wish_list.html', {'wishlist_items': wishlist_items,'product_types':product_types,'categories':categories,'cart_count':cart_count,'wishlist_count':wishlist_count})


@login_required(login_url='signin')
def remove_from_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
    if wishlist_item.exists():
        wishlist_item.delete()
    return redirect('wishlist')



def add_product_type(request):
    if request.method == 'POST':
        product_type_name = request.POST.get('product_type_name')
        product_type_name_ar = request.POST.get('product_type_name_ar')

        if product_type_name and product_type_name_ar:
            product_type = ProductType()
            setattr(product_type, 'name', product_type_name)
            setattr(product_type, 'name_ar', product_type_name_ar)
            product_type.save()

        return redirect('add_product_type')

    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    return render(request, 'add_product_type.html', {'product_types': product_types, 'categories': categories})



def delete_product_type(request, delet_product_type):
    product_type = get_object_or_404(ProductType, id=delet_product_type)
    
    product_type.delete()  # Delete the product type
    
    return redirect('add_product_type')  # Redirect to the list page



def edit_product_type(request, edit_type):
    product_type = get_object_or_404(ProductType, id=edit_type)

    if request.method == 'POST':
        product_type_name = request.POST.get('product_type_name')
        product_type_name_ar = request.POST.get('product_type_name_ar')

        if product_type_name and product_type_name_ar:
            setattr(product_type, 'name', product_type_name)
            setattr(product_type, 'name_ar', product_type_name_ar)
            product_type.save()  # Save changes to the product type
        
        return redirect('add_product_type')  # Redirect to the list page

    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    return render(request, 'edit_product_type.html', {'product_type': product_type, 'product_types': product_types, 'categories': categories})

def add_category(request):
    if request.method == 'POST':
        product_type_id = request.POST.get('product_type')
        category_name = request.POST.get('category_name')
        category_name_ar = request.POST.get('category_name_ar')

        if product_type_id and category_name and category_name_ar:
            category = Category()
            setattr(category, 'product_type_id', product_type_id)
            setattr(category, 'name', category_name)
            setattr(category, 'name_ar', category_name_ar)
            category.save()

        return redirect('add_category')

    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    return render(request, 'add_category.html', {'product_types': product_types, 'categories': categories})



def p_delete_form(request,pk):
    edit=Product.objects.get(id=pk)
    edit.delete()
    return redirect('add_product')


def p_delete_category(request,pk):
    edit=Category.objects.get(id=pk)
    edit.delete()
    return redirect('add_category')


def add_product(request):
    if request.method == 'POST':
        product_type_id = request.POST.get('product_type')
        category_id = request.POST.get('category')
        heading = request.POST.get('heading')
        heading_ar = request.POST.get('heading_ar')
        description = request.POST.get('description')
        description_ar = request.POST.get('description_ar')
        original_price = request.POST.get('original_price')
        discount_price = request.POST.get('discount_price')
        stock = request.POST.get('stock')
        delivery_charge = request.POST.get('delivery_charge', 0.00)

        # Create product instance
        product = Product.objects.create(
            product_type_id=product_type_id,
            category_id=category_id,
            heading=heading,
            heading_ar=heading_ar,
            description=description,
            description_ar=description_ar,
            original_price=original_price,
            discount_price=discount_price,
            stock=stock,
            delivery_charge=delivery_charge
        )

        # Handle multiple images
        images = request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return redirect('add_product')
    else:
        product_types = ProductType.objects.all()
        categories = Category.objects.all()
        products = Product.objects.all()
        reversed_order = reversed(list(products))
        return render(request, 'add_product.html', {
            'product_types': product_types,
            'categories': categories,
            'products': reversed_order,
        })

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.product_type_id = request.POST.get('product_type', product.product_type_id)
        product.category_id = request.POST.get('category', product.category_id)
        product.heading = request.POST.get('heading', product.heading)
        product.heading_ar = request.POST.get('heading_ar', product.heading_ar)
        product.description = request.POST.get('description', product.description)
        product.description_ar = request.POST.get('description_ar', product.description_ar)
        product.original_price = float(request.POST.get('original_price', product.original_price))
        product.discount_price = float(request.POST.get('discount_price', product.discount_price))
        product.stock = int(request.POST.get('stock', product.stock))
        product.delivery_charge = float(request.POST.get('delivery_charge', product.delivery_charge))
        product.save()

        # Handle new images if updated
        new_images = request.FILES.getlist('images')
        for image in new_images:
            ProductImage.objects.create(product=product, image=image)

        return redirect('add_product')

    context = {
        'product': product,
        'product_types': ProductType.objects.all(),
        'categories': Category.objects.all(),
    }

    return render(request, 'edit_product.html', context)


def signup_page(request):
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    return render(request, 'sign_in.html', {'product_types': product_types, 'categories': categories})

def usercreate(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['confirm_password']
        email = request.POST['email']
        phone_no = request.POST['phone']

        if password == cpassword:
            # Check if the username is already taken
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This username is already taken. Please choose a different one.')
                return redirect('signup_page')
            else:
                # Create the user and profile
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email
                )
                user.save()

                user_profile = UserProfile.objects.create(
                    user=user,
                    phone_number=phone_no
                )
                user_profile.save()
                print('Succeed....')
        else:
            messages.info(request, 'Passwords do not match!')
            print('Passwords do not match')
            return redirect('signup_page')

        return redirect('login_page')
    else:
        return render(request, 'sign_in.html')


def login_page(request):
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    cart_count = 0
    wishlist_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request,'login.html',{'product_types':product_types,'categories':categories,'cart_count':cart_count,'wishlist_count':wishlist_count})




def signin(request):
    if request.method == 'POST':
        # Get the username (or email) and password from the request, with default values to avoid KeyError
        username = request.POST.get('username', '')  # Assuming 'username' is the email
        password = request.POST.get('password', '')

        # Authenticate the user with the provided credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User authenticated successfully
            login(request, user)  # Log in the user

            # Redirect based on user type
            if user.is_staff:
                return redirect('admin_page')  # Redirect admin users to the admin page
            else:
                return redirect('homepage')  # Redirect regular users to the index page
        else:
            # Authentication failed, show an error message
            messages.error(request, 'Invalid credentials. Please try again.')
            # Render the login page with the error message
            return render(request, 'login.html', context={'error': 'Invalid credentials'})

    # If not a POST request, render the login page
    return render(request, 'login.html')


def setnewpassword(request):

    if request.method=='POST':
        email_or_username = request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        if password==cpassword:

            c = User.objects.filter(Q(username = email_or_username)|Q(email = email_or_username)).first()
            c.set_password(password)
            c.save()

        return redirect('login_page' )
        
    else:
        categories = Category.objects.all()
        user = request.user.id
        carts = Cart.objects.filter(user=user)
        total_quantity = sum(cart.quantity for cart in carts)
        return render(request, 'setpassword.html',{'cart_quantity': total_quantity,'categories': categories,'carts': carts,})


@login_required(login_url='signin')
def admin_page(request):
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    return render(request,'admin.html',{'product_types':product_types,'categories':categories})



def cart_page(request):
    carts = []
    subtotal = 0
    total_price = 0
    cart_count = 0
    total_delivery_charge = 0

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user).order_by('-id')
        for cart in carts:
            subtotal += cart.product.discount_price * cart.quantity
            total_delivery_charge += cart.product.delivery_charge * cart.quantity
        total_price = subtotal + total_delivery_charge
        cart_count = sum(cart.quantity for cart in carts)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        session_cart = request.session.get('cart', {})
        product_ids = [int(key) for key in session_cart.keys()]
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            quantity = session_cart[str(product.id)]['quantity']
            subtotal += product.discount_price * quantity
            total_delivery_charge += product.delivery_charge * quantity
            carts.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.discount_price * quantity
            })
        total_price = subtotal + total_delivery_charge
        cart_count = sum(item['quantity'] for item in session_cart.values())
        wishlist_count = 0  # No wishlist for unauthenticated users

    product_types = ProductType.objects.all()
    categories = Category.objects.all()

    return render(request, 'cart.html', {
        'carts': carts,
        'total_price': total_price,
        'subtotal': subtotal,
        'total_delivery_charge': total_delivery_charge,
        'product_types': product_types,
        'categories': categories,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    })





@login_required(login_url='signin')
def remove_from_cart(request, pk):
    cart = Cart.objects.filter(id=pk, user=request.user).first()
    if cart:
        cart.delete()
    return redirect('cart_page')

@require_POST
def remove_from_session_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return JsonResponse({'success': True})
    

@login_required(login_url='signin')
def update_cart(request,pk):
    cart = Cart.objects.filter(id=pk, user=request.user).first()
    if cart and request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.quantity = quantity
        cart.save()
    return redirect('cart_page')


def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))  # Get quantity from form, default to 1

        if request.user.is_authenticated:
            cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()
        else:
            cart = request.session.get('cart', {})
            if str(pk) in cart:
                cart[str(pk)]['quantity'] += quantity
            else:
                cart[str(pk)] = {
                    'product_id': pk,
                    'quantity': quantity
                }
            request.session['cart'] = cart

    return redirect('cart_page')



@login_required(login_url='signin')
def checkout_page(request):
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    carts = Cart.objects.filter(user=request.user)
    subtotal = sum(cart.product.discount_price * cart.quantity for cart in carts)
    total_delivery_charge = sum(cart.product.delivery_charge for cart in carts)
    total_price = subtotal + total_delivery_charge
    cart_count = 0
    wishlist_count = 0
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        country = request.POST['country']
        address = request.POST['address']
        city = request.POST['city']
        phone = request.POST['phone']
        email = request.POST['email']

        customer = Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            country=country,
            address=address,
            city=city,
            phone=phone,
            email=email
        )

        order = Order.objects.create(
            customer=customer,
            user=request.user,
            subtotal=subtotal,
            delivery_charge=total_delivery_charge  # Save delivery charge
        )

        for cart in carts:
            OrderItem.objects.create(
                order=order,
                product=cart.product,
                quantity=cart.quantity,
                price=cart.product.discount_price
            )

        # Clear the cart after creating the order
        carts.delete()

        # Redirect to payment gateway page
        return redirect('payment_gateway', order_id=order.id)

    context = {
        'carts': carts,
        'subtotal': subtotal,
        'total_delivery_charge': total_delivery_charge,
        'total_price': total_price,
        'product_types': product_types,
        'categories': categories,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    }
    return render(request, 'checkout_page.html', context)




def send_order_confirmation_email(email, order_id, total_price):
    subject = 'Order Confirmation'
    message = f'Thank you for your order! Your order ID is {order_id} and the total price is ${total_price}.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

def send_order_failure_email(email, order_id):
    subject = 'Order Failed'
    message = f'Unfortunately, your order with ID {order_id} could not be completed. Please try again.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)



@login_required(login_url='signin')
def payment_gateway(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user != request.user:
        return HttpResponseForbidden("You do not have permission to access this order.")
    
    total_price = order.subtotal + order.delivery_charge  # Calculate total price including delivery charge
    
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    cart_count = 0
    wishlist_count = 0

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    context = {
        'order': order,
        'product_types': product_types,
        'categories': categories,
        'total_price': total_price,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
    }
    return render(request, 'payment_gateway.html', context)



@login_required(login_url='signin')
def payment_redirect(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Retrieve the payment status from Tap Payments
    payment_id = request.GET.get('tap_id')
    url = f"https://api.tap.company/v2/charges/{payment_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.TAP_PAYMENT_SECRET_KEY}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        payment = response.json()
        if payment['status'] == 'CAPTURED':
            # Payment was successful
            order.status = 'Paid'
            order.save()

            # Decrease stock for each product in the order
            order_items = OrderItem.objects.filter(order=order)
            for item in order_items:
                product = item.product
                print(f"Product: {product}, Method exists: {hasattr(product, 'decrease_stock')}")
                try:
                    product.decrease_stock(item.quantity)
                except ValueError as e:
                    return HttpResponse(f"An error occurred: {str(e)}")

            # Clear the user's cart
            Cart.objects.filter(user=request.user).delete()

            # Send success email
            send_order_confirmation_email(order.customer.email, order.id, order.subtotal)

            return redirect('payment_success')
        else:
            # Payment failed
            order.status = 'Failed'
            order.save()

            # Send failure email
            send_order_failure_email(order.customer.email, order.id)
            
            return render(request, 'payment_failed.html', {'order': order})
    else:
        return HttpResponse(f"An error occurred: {response.json().get('message', 'Unknown error')}")


def payment_success(request):
    return render(request,'payment_sucess.html')


@login_required(login_url='signin')
def order_page(request):
    orders = Order.objects.filter(user=request.user).exclude(status='Failed').prefetch_related('items__product__images').order_by('-created_at')
    for order in orders:
        print(f"Order ID: {order.id}, Status: {order.status}")
    return render(request, 'order_page.html', {'orders': orders})





@login_required(login_url='signin')
def manage_orders(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        if order_id and new_status:
            try:
                order = Order.objects.get(id=order_id)
                order.status = new_status
                order.save()
            except Order.DoesNotExist:
                pass  # Handle the error as necessary

    order_items = OrderItem.objects.all().select_related('order', 'product').prefetch_related('product__images').order_by('-order__created_at')
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    return render(request, 'admin_manage_orders.html', {'order_items': order_items,'product_types':product_types,'categories':categories})




@login_required(login_url='signin')
def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user != request.user:
        return HttpResponseForbidden("You do not have permission to access this order.")

    # Convert total_price from Decimal to float
    total_price = float(order.subtotal + order.delivery_charge)
    # Tap Payments API endpoint
    url = "https://api.tap.company/v2/charges"

    # Payment request payload
    payload = {
        "amount": total_price,  # Use the converted amount
        "currency": "SAR",
        "threeDSecure": True,
        "save_card": False,
        "description": f"Order #{order.id}",
        "statement_descriptor": "Order Payment",
        "customer": {
            "first_name": order.customer.first_name,
            "last_name": order.customer.last_name,
            "email": order.customer.email,
            "phone": {
                "country_code": "966",
                "number": order.customer.phone
            }
        },
        "source": {"id": "src_all"},
        "redirect": {
            "url": request.build_absolute_uri(reverse('payment_redirect', args=[order.id]))
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.TAP_PAYMENT_SECRET_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        payment_url = response.json()['transaction']['url']
        return redirect(payment_url)
    else:
        return HttpResponse(f"An error occurred: {response.json().get('message', 'Unknown error')}")


@login_required(login_url='signin')
@csrf_exempt
def update_cart_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart_id = data.get('cart_id')
        quantity = data.get('quantity')

        try:
            cart_item = Cart.objects.get(id=cart_id, user=request.user)
            cart_item.quantity = quantity
            cart_item.save()

            # Calculate updated totals
            carts = Cart.objects.filter(user=request.user)
            subtotal = sum(cart.product.discount_price * cart.quantity for cart in carts)
            total_delivery_charge = sum(cart.product.delivery_charge * cart.quantity for cart in carts)
            total_price = subtotal + total_delivery_charge

            return JsonResponse({
                'status': 'success',
                'subtotal': subtotal,
                'total_delivery_charge': total_delivery_charge,
                'total_price': total_price
            })
        except Cart.DoesNotExist:
            return JsonResponse({'status': 'fail', 'error': 'Cart item does not exist'}, status=400)

    return JsonResponse({'status': 'fail'}, status=400)



def category_detail_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(products, 20)  # Show 20 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cart_count = 0
    wishlist_count = 0
 
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    for product in products:
        product.final_price = product.discount_price or product.original_price

    return render(request, 'category_page.html', {
        'category': category,
        'products': products,
        'product_types':product_types,
        'categories':categories,
        'cart_count':cart_count,
        'wishlist_count':wishlist_count,
        'page_obj':page_obj,


    })

def search_results(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(heading__icontains=query) | 
        Q(description__icontains=query)
    ) if query else None
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    cart_count = 0
    wishlist_count = 0
 
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    context = {
        'products': products,
        'query': query,
        'product_types':product_types,
        'categories':categories,
        'cart_count':cart_count,
        'wishlist_count':wishlist_count


    }
    return render(request, 'search_results.html', context)


def add_video(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        video_file = request.FILES.get('video_file')
        
        if product_id and video_file:
            product = Product.objects.get(id=product_id)
            Video.objects.create(product=product, video_file=video_file)
            return redirect('add_video')  # Redirect after posting

    products = Product.objects.all()  # Get all products to populate the select box
    videos = Video.objects.all().select_related('product')
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    return render(request, 'add_video.html', {'products': products,'videos':videos,'product_types':product_types,'categories':categories})


def delete_video_section(request, video):
    jumbotrons = get_object_or_404(Video, id=video)  # Get the Swiper slide by ID
    
    jumbotrons.delete()  # Delete the Swiper slide
    return redirect('add_video')


def logout(request):
	auth.logout(request)
	return redirect('/')


def edit_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        product_id = request.POST.get('product')
        video_file = request.FILES.get('video_file') if 'video_file' in request.FILES else None

        if product_id:
            video.product_id = product_id
            if video_file:
                video.video_file = video_file
            video.save()
            return redirect('add_video')  # Redirect to the video list view after successful update

    products = Product.objects.all()  # Fetch all products for dropdown
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    return render(request, 'edit_video.html', {'video': video, 'products': products,'product_types':product_types,'categories':categories})


def add_find_logo(request):
    if request.method == 'POST':
        
        image = request.FILES.get('image')
        alt_text = request.POST.get('alt_text')

        # Create the ingredient with name and image
        ClientLogo.objects.create(alt_text=alt_text, image=image)
        
        return redirect('add_find_logo')  # Redirect after successful addition
    
    logos = ClientLogo.objects.all()  # Retrieve all ingredients
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    return render(request, 'add_find_logo.html',{'logos':logos,'product_types':product_types,'categories':categories})  # Render form for adding


def edit_find_logo(request, slide_id):
    logo = get_object_or_404(ClientLogo, id=slide_id)  # Get the Swiper slide by ID
    product_types = ProductType.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':  # Handle form submission for editing
        image = request.FILES.get('image')  # Updated image
        alt_text = request.POST.get('alt_text')  # Updated button text
        

        # Update the Swiper slide fields
        if image:
            logo.image = image
        logo.alt_text = alt_text
        
        logo.save()  # Save the changes
        return redirect('add_find_logo')  # Redirect to the list page

    return render(request, 'edit_find_logo.html', {'logo': logo,'product_types':product_types,'categories':categories})


def delete_find_logo(request, slide_id):
    slide = get_object_or_404(ClientLogo, id=slide_id)  # Get the Swiper slide by ID
    
    slide.delete()  # Delete the Swiper slide
    return redirect('add_find_logo')


def product_type_view(request,product_type_id):
    product_type = get_object_or_404(ProductType, id=product_type_id)
    products = Product.objects.filter(product_type=product_type)
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(products, 20)  # Show 20 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cart_count = 0
    wishlist_count = 0
 
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    for product in products:
        product.final_price = product.discount_price or product.original_price

    return render(request, 'product_type_page.html', {
        'product_type': product_type,
        'products': products,
        'product_types':product_types,
        'categories':categories,
        'cart_count':cart_count,
        'wishlist_count':wishlist_count,
        'page_obj':page_obj,


    })


def add_desktop_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        alt_text = request.POST.get('alt_text', '')
        
        DesktopCarouselImage.objects.create(image=image, alt_text=alt_text)
        return redirect('add_desktop_image')
    desktop_images = DesktopCarouselImage.objects.all()
    product_types = ProductType.objects.all()
    categories = Category.objects.all()

    return render(request, 'add_desktop_image.html',{'desktop_images':desktop_images,'product_types':product_types,'categories':categories})

def add_mobile_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        alt_text = request.POST.get('alt_text', '')
        
        MobileCarouselImage.objects.create(image=image, alt_text=alt_text)
        return redirect('add_mobile_image')
    mobile_images = MobileCarouselImage.objects.all()
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    return render(request, 'add_mobile_image.html',{'mobile_images':mobile_images,'product_types':product_types,'categories':categories})


def delete_desktop_image(request, image_id):
    image = get_object_or_404(DesktopCarouselImage, id=image_id)
    image.delete()
    return redirect('add_desktop_image')

def delete_mobile_image(request, image_id):
    image = get_object_or_404(MobileCarouselImage, id=image_id)
    image.delete()
    return redirect('add_mobile_image')


def edit_desktop_image(request, image_id):
    image = get_object_or_404(DesktopCarouselImage, id=image_id)
    if request.method == 'POST' and request.FILES['image']:
        image.image = request.FILES['image']
        image.alt_text = request.POST.get('alt_text', '')
        image.save()
        return redirect('add_desktop_image')
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    return render(request, 'edit_desktop_image.html', {'image': image,'product_types':product_types,'categories':categories})



def edit_mobile_image(request, image_id):
    image = get_object_or_404(MobileCarouselImage, id=image_id)
    if request.method == 'POST' and request.FILES['image']:
        image.image = request.FILES['image']
        image.alt_text = request.POST.get('alt_text', '')
        image.save()
        return redirect('add_mobile_image')
    return render(request, 'edit_mobile_image.html', {'image': image})



def add_link(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        name_ar = request.POST.get('name_ar')  # Get the Arabic name from the form
        website = request.POST.get('website')

        # Basic validation
       
        link = Links(name=name,name_ar=name_ar, website=website)
        link.save()

        return redirect('add_link')  # Replace with your desired success URL
    links = Links.objects.all()
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
        

    return render(request, 'add_link.html',{'links':links,'product_types':product_types,'categories':categories})



def edit_link(request, link_id):
    # Fetch the existing link from the database
    link = get_object_or_404(Links, id=link_id)

    if request.method == 'POST':
        # Get the updated data from the form
        name = request.POST.get('name')
        name_ar = request.POST.get('name_ar')
        website = request.POST.get('website')

        # Update the link object
        link.name = name
        link.name_ar = name_ar
        link.website = website
        link.save()  # Save the updated link

        # Redirect to a success page or back to the list of links
        return redirect('add_link')  # Or wherever you'd like to redirect after editing

    # Render the edit form with the existing link data
    return render(request, 'edit_link.html', {'link': link})




def delete_link(request, link_id):
    link = get_object_or_404(Links, id=link_id)
    link.delete()
    return redirect('add_link') 