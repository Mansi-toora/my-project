from django.shortcuts import render,HttpResponse,redirect
from.models import*
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404, redirect
from.models import*
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')
def shop(request):
    
    men_products = Product.objects.filter(category='men')
    women_products = Product.objects.filter(category='women')
    kids_products = Product.objects.filter(category='kids')
    product=Product.objects.all()
    return render(request, 'shop.html', {
        'men_products': men_products,
        'women_products': women_products,
        'kids_products': kids_products,
        "product":product
    })
@login_required(login_url='login')
def cart(request):
    # Get cart items for the authenticated user
    cart_items = CartItem.objects.filter(user=request.user)
    
    # Calculate total price
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    # Calculate cart item count
    cart_item_count = sum(item.quantity for item in cart_items)
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_item_count': cart_item_count
    })

def services(request):
    return render(request,'services.html')

def blog(request):
    return render(request,'blog.html')

def signup(request):
    if request.method=='POST':
        name=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        if password==cpassword:
            User.objects.create_user(username=name,email=email,password=password).save()
            return redirect('logins')
        else:
            return HttpResponse("Password Didn't match!")
    return render(request,'signup.html')


def logins(request):
     if request.method=='POST':
        name=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=name,password=password)
        if user:
            login(request,user)
            return redirect(home)
        else:
            return HttpResponse("Invalid credentials!")
     return render(request,'login.html')

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        phone=request.POST['phone']
        dob=request.POST['dob']
        gender=request.POST['gender']
        address=request.POST['address']
        hashed_password = make_password(password)
        obj=student(Name=name,Email=email,Password=hashed_password,Phone=phone,DOB=dob,Gender=gender,Address=address)
        obj.save()
        return HttpResponse("Data Inserted")
        
    return render(request,'contact.html')


def fetch(request):
    dd=student.objects.all()
    return render(request,'fetch.html',{'d':dd})


def update(request,id):
    dd=student.objects.get(id=id)
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        phone=request.POST['phone']
        dob=request.POST['dob']
        gender=request.POST['gender']
        address=request.POST['address']
        dd.Name=name
        dd.Email=email
        dd.Password=password
        dd.Phone=phone
        dd.DOB=dob
        dd.Gender=gender
        dd.Address=address
        dd.save()
        return redirect(fetch)
    return render(request,'update.html',{'dd':dd})


def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        if password==cpassword:
            User.objects.create_user(username=username,email=email,password=password).save()
            return redirect(logins)
        else:
            return HttpResponse("password not match!")
    return render(request,'signup.html')


# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart = request.session.get('cart', {})
#     cart[str(product_id)] = cart.get(str(product_id), 0) + 1
#     request.session['cart'] = cart
#     return redirect('cart')  # Redirect to cart page

def product_detail(request, id):
    dd = Product.objects.get(id=id)
    p=Product.objects.all()
    
    if request.method == 'POST':
        qty = int(request.POST['quantity'])
        size = request.POST.get('size')  # Get size from form
        
        # Save CartItem with size
        x = CartItem(product=dd, quantity=qty, size=size, user=request.user)
        x.save()
        return redirect(cart)  # Make sure you have a cart URL named 'cart'
    return render(request, 'product_details.html', {'dd': dd,'p':p})

def remove_from_cart(request, id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    return redirect(cart)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, F
from .models import Order, CartItem, OrderItem
from django.contrib.auth.models import User

def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        payment_method = request.POST.get('payment_method')
        card_number = request.POST.get('card_number') if payment_method == 'online' else None
        expiry_date = request.POST.get('expiry_date') if payment_method == 'online' else None
        cvv = request.POST.get('cvv') if payment_method == 'online' else None
        upi_id = request.POST.get('upi_id') if payment_method == 'upi' else None

        if not cart_items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect('cart')

        # Create order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            payment_method=payment_method,
            card_number=card_number,
            expiry_date=expiry_date,
            cvv=cvv,
            upi_id=upi_id
        )

        # Create OrderItems without cart_item
        for cart_item in cart_items:
            OrderItem.objects.create(
        order=order,
        product=cart_item.product,
        quantity=cart_item.quantity,
        size=cart_item.size,  # Save the selected size
        price=cart_item.product.price
    )

        # Clear cart
        cart_items.delete()


        messages.success(request, "Order placed successfully!")
        return redirect('order_success', order_id=order.id)
   
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        
    })

def thankyou(request):
    return render(request, 'thankyou.html')

def order_success_view(request, order_id):
    # Fetch the order
    order = get_object_or_404(Order, id=order_id)
    
    # Fetch all items related to this order
    order_items = OrderItem.objects.filter(order=order)
    
    # Calculate total price
    total_price = sum(item.price * item.quantity for item in order_items)
    
    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price
    }
    
    return render(request, 'order_success.html', context)

def logout_view(request):
    """Log out the current user and redirect to login page"""
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login') 


@login_required
def orders_view(request):
    # Get all orders for the current user
    user_orders = Order.objects.filter(user=request.user).order_by('-id')
    
    context = {
        'orders': user_orders,
    }
    return render(request, 'orders.html', context)
