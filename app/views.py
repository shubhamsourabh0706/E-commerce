from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q

from django.contrib.auth import authenticate,login,logout
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
import json

# Create your views here.
def home(request):
    total_product = 0
    data = Category.objects.all()
    carsouel = Carousel.objects.all()
    
    mobile = Product.objects.filter(category='M')
    fashion = Product.objects.filter(category='F')
    ele = Product.objects.filter(category='E')
    app = Product.objects.filter(category='A')
    fur = Product.objects.filter(category='F')
    grocery = Product.objects.filter(category='G')
    if request.user.is_authenticated:
        total_product = len(Cart.objects.filter(user=request.user))
    
    # Truncate titles for all products
    
    
    param = {
        "data": data,
        "carsouel": carsouel,
        "mobile": mobile,
        "fashion": fashion,
        "ele": ele,
        "app": app,
        "grocery": grocery,
        "fur": fur,
        "total_product":total_product
         # Pass truncated titles to the template
    }
    return render(request, 'home.html', param)

def product_detail(request):
    total_product = 0
    eid = request.GET.get('id')
    data = Product.objects.get(id=eid)
    product_is_in_cart = False
    if request.user.is_authenticated:
        
        total_product = len(Cart.objects.filter(user=request.user))
        product_is_in_cart = Cart.objects.filter(Q(product=data.id) & Q(user=request.user)).exists()
    param = {"product":data,"product_is_in_cart":product_is_in_cart,"total_product":total_product}
    return render(request,'product_detail.html',param)

def admin_login(request):
    return render(request,'admin_login.html')

def admin_data(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        try:
            if user.is_staff:
                login(request,user)
                return admin_dashboard(request)
            else:
                param={"msg":"Invalid Credentials"}
                return render(request,'admin_login.html',param)
        except Exception as e:
            param = {"msg":"Invalid Credentials"}
            return render(request,'admin_login.html',param)
    else:
        return render(request,'admin_login.html')
@login_required   
def add_category(request):
    return render(request,'add_category.html')
@login_required  
def category_data(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES['image']
        Category.objects.create(name=name,images=image)
        return render(request,"view_category.html")
    else:
        return render(request,'add_category.html')
@login_required      
def view_category(request):
    category = Category.objects.all()
    param = {"data":category}
    return render(request,'view_category.html',param)
@login_required  
def del_category(request):
    id = request.GET.get('id')
    Category.objects.filter(id=id).delete()
    return view_category(request)
@login_required  
def edit_category(request):
    id = request.GET.get('id')
    category = Category.objects.get(id=id)
    param = {"category":category}
    return render(request,'edit_category.html',param)
@login_required  
def update_category(request,):
    id = request.POST.get('id')
    category = Category.objects.get(id=id)
    if request.method == 'POST':
         name = request.POST['name']
         try:
            image = request.FILES['image']
            category.images = image
            category.save()
         except Exception as e:
             pass
         Category.objects.filter(id=id).update(name=name)
         return view_category(request)
    else:
        return render(request,'edit_category.html')
    
@login_required     
def add_product(request):
    data = CATEGORY_CHOICES
    
    param ={"data":data}

    return render(request,'add_product.html',param)
@login_required  
def product_data(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        title = request.POST.get('title')
        sp = request.POST.get('sp')
        dp = request.POST.get('dp')
        brand = request.POST.get('brand')
        desc = request.POST.get('desc')
        
        # Check if 'images' exists in request.FILES
        if 'images' in request.FILES:
            images = request.FILES['images']
            Product.objects.create(category=category, title=title, selling_price=sp, dicounted_price=dp, brand=brand, description=desc, images=images)
            return view_product(request)
        else:
            # Handle the case where 'images' is not present
            # You can return an error message or redirect the user to a page to upload images
            return HttpResponse("Please upload images.")
@login_required         
def view_product(request):
    data = Product.objects.all()
    param = {"data":data}
    return render(request,'view_product.html',param)
@login_required  
def del_product(request):
    id = request.GET.get('id')
    Product.objects.filter(id=id).delete()
    return view_product(request)
        
@login_required          
def edit_product(request):
    category = CATEGORY_CHOICES
    id = request.GET.get('id')
    data = Product.objects.get(id=id)
    param = {"data":data,"category":category}
    return render(request,'edit_product.html',param)


#there is a error we have to fix

@login_required  
def update_product(request):
    if request.method == "POST":
        try:
            id = request.POST.get('id')
            title = request.POST.get('title')
            sp = request.POST.get('sp')
            category = request.POST.get('category')
            dp = request.POST.get('dp')
            brand = request.POST.get('brand')
            desc = request.POST.get('desc')
            image = request.FILES.get('image')  # Use get() to avoid KeyError if image is not provided
            
            # Update the product
            product = Product.objects.get(id=id)
            product.title = title
            product.selling_price = sp
            product.dicounted_price = dp
            product.category = category
            product.description = desc
            product.brand = brand
            if image:
                product.image = image
            product.save()
            print("Received image:", image)
            
            return redirect('view_product')
        except ObjectDoesNotExist as e:
            return HttpResponse("Product not found.")
        except Exception as e:
            return HttpResponse("An error occurred while processing the form data.")
    
    return render(request, 'edit_product.html')

def create_account(request):
    return render(request,'create_account.html')

def registration(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpwd = request.POST.get('cpwd')
        if (password == cpwd):
            user = User.objects.create_user(username=email,first_name=fname, last_name=lname,password=password)
            return render(request,"user_login.html")
        else:
            param={"msg":"Password did not match..."}
            return render(request,'create_account.html',param)
    else:
        param = {"msg": "Please provide correct information"}
        return render(request,'create_account.html',param)
    
def user_login(request):
    return render(request,'user_login.html')

def login_data(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user :
            login(request,user)
            return home(request)
        else:
            param = {"msg":"Username and Password did not match"}
            return render(request,'user_login.html',param)
    else:
         param = {"msg":"Please Enter your username and password"}
         return render(request,'user_login.html',param)
        
def logout_user(request):
    logout(request)
    return home(request)

@login_required  
def user_profile(request):
    total_product = 0
    profile = Profile.objects.filter(user=request.user)
    if request.user.is_authenticated:
        total_product = len(Cart.objects.filter(user=request.user))
    param = {"profile":profile,"active":"btn-primary","total_product":total_product}
    return render(request,'user_profile.html',param)

@login_required  
def update_profile(request):
    state = indian_states_tuple
    total_product = 0
    if request.user.is_authenticated:
        total_product = len(Cart.objects.filter(user=request.user))
    
    return render(request,'profile.html',{"state":state,"total_product":total_product})
@login_required  
def profile_data(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        Profile.objects.create(user=request.user,name=name,contact=phone,locality=locality,cities=city,state=state,zipcode=pincode)
        return user_profile(request)
    else:
        
        return update_profile(request)
    
@login_required      
def change_password(request):
    total_product = 0
    if request.user.is_authenticated:
        total_product = len(Cart.objects.filter(user=request.user))
    return render(request,'change_password.html',{"total_product":total_product})

@login_required  
def update_password(request):
    if request.method == "POST":
        o = request.POST.get('o')  # Old password
        n = request.POST.get('n')  # New password
        c = request.POST.get('c')  # Confirm password

        # Authenticate the user with old password
        user = authenticate(request=request, username=request.user.username, password=o)

        if user is not None:
            # Check if new and confirm passwords match
            if n == c:
                # Set the new password
                user.set_password(n)
                user.save()
                return redirect('home')  # Redirect to home page after successful password change
            else:
                # Passwords don't match
                return render(request, 'change_password.html', {'msg': 'New passwords did not match'})
        else:
            # Invalid old password
            return render(request, 'change_password.html', {'msg': 'Invalid old password'})
    else:
        # Request method is not POST (e.g., GET request)
        return render(request, 'change_password.html', {'msg': 'Please fill in the details'})
    
@login_required     
def feedback(request):
   total_product = 0
   if request.user.is_authenticated:
       total_product = len(Cart.objects.filter(user=request.user))
   return render(request,'feedback.html',{"total_product":total_product})

@login_required  
def feedback_data(request):
    if request.method == 'POST':
        sub = request.POST.get('sub')
        msg = request.POST.get('msg')
        Feedback.objects.create(user=request.user,subject=sub,message=msg)
        return redirect('home')
    else:
        param = {"msg":"Please enter detail"}
        return render(request,'feedback.html',param)
    
    
def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        
        # If the request is AJAX, return JSON response with cart count
        
        
        # If the request is not AJAX, perform a redirect
        return redirect('show_cart')
    else:
        # If user is not authenticated, return the login page
        return user_login(request)
    







def show_cart(request):
    if request.user.is_authenticated:
        total_product=0
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 49
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        total_product=len(cart)
        if cart_product:
            for p in cart_product:
                tempAmount = (p.quantity * p.product.dicounted_price)
                amount += tempAmount
                total_amount = shipping_amount + amount

            param = {"cart": cart, "amount":amount,"totalAmount":total_amount,"shipping_amount":shipping_amount,"total_product":total_product}
            return render(request, 'showCart.html', param)
        else:
            return render(request,"empty_cart.html")
    else:
        return user_login(request)
        
@login_required          
def plusCart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 49
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempAmount = (p.quantity * p.product.dicounted_price)
                amount += tempAmount
                
            data = {
                "quantity":  c.quantity,
                "amount": amount,
                "total_amount":amount +shipping_amount
            }
            return JsonResponse(data)
        
@login_required          
def minusCart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -=1
        c.save()
        amount = 0.0
        shipping_amount = 49
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempAmount = (p.quantity * p.product.dicounted_price)
                amount += tempAmount
                
            data = {
                "quantity": c.quantity,
                "amount" : amount,
                "total_amount" : amount + shipping_amount
            }
            return JsonResponse(data)
        
@login_required          
def removeCart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 49
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempAmount = (p.quantity * p.product.dicounted_price)
                amount += tempAmount
                
            data = {
                "amount":amount,
                "total_amount":amount + shipping_amount
            }
            return JsonResponse(data)
        
@login_required          
def check_out(request):
    total_product =0
    add = Profile.objects.filter(user=request.user)
    cart_items = Cart.objects.filter(user=request.user)
    amount = 0.0
    shipping_amount = 49
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempAmount = (p.quantity * p.product.dicounted_price)
            amount += tempAmount
        total_amount = amount + shipping_amount
    if request.user.is_authenticated:
        total_product = len(cart_items)
    param ={"add":add, "carts":cart_items,"total_amount":total_amount,"total_product":total_product}

    return render(request,'check_out.html',param)

@login_required              
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Profile.objects.get(id=custid)

    # Get cart items for the user
    cart = Cart.objects.filter(user=user)

    order_details = []
    total_amount = 0

    # Calculate order details and total amount
    for c in cart:
        order_details.append({
            'product': c.product.title,
            'quantity': c.quantity,
            'price': c.product.dicounted_price * c.quantity  # Make sure to use the correct attribute
        })
        total_amount += c.product.dicounted_price * c.quantity

    # Add any additional charges
    total_amount += 49  # Add fixed amount
    
    # Save bookings
    for c in cart:
        Booking.objects.create(
            user=user,
            customer=customer,
            product=c.product,
            quantity=c.quantity
        )

    # Delete cart items
    cart.delete()

    # Send confirmation email
    subject = 'Order Confirmation'
    html_message = render_to_string('confirmation_email.html', {'order_details': order_details,
        'total_amount': total_amount,

        
         # Assuming you have a delivery date field in your Booking model
        })
    plain_message = strip_tags(html_message)  # Strip HTML tags for plain text message
    from_email = settings.EMAIL_HOST_USER
    to_email = [request.user.username]
    print(to_email)  # Use the email field of the User model

    try:
        # Send email
        send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
        messages.success(request, 'Order placed successfully. Check your email for confirmation.')
    except Exception as e:
        messages.error(request, 'Failed to send confirmation email. Please contact support.')

    return redirect('orders')

@login_required  
def orders(request):
    total_product =0
    order = Booking.objects.filter(user=request.user)
    if request.user.is_authenticated:
        total_product = len(Cart.objects.filter(user=request.user))
    param = {"order":order,"total_product":total_product}

    return render(request,'order.html',param)

            
@login_required  
def return_product(request):
    id = request.GET.get('id')
    order = Booking.objects.get(id=id)
    order.status = 7
    order.save()
    return orders(request)

@login_required  
def cancel_product(request):
    id = request.GET.get('id')
    order = Booking.objects.get(id=id)
    order.status = 6
    order.save()
    return orders(request)

def manage_feedback(request):
    action = request.GET.get('action',0)
    feedback = Feedback.objects.filter(status=int(action))
    param = {"feedback":feedback}
    return render(request,'manage_feedback.html',param)

def delete_feedback(request):
    id = request.GET.get('id')
    Feedback.objects.get(id=id).delete()
    return manage_feedback(request)

def read_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.status = 1
    feedback.save()
    return HttpResponse(json.dumps({'id':1, 'status':'success'}), content_type="application/json")

def manage_order(request):
    action = request.GET.get('action',0)
    order = Booking.objects.filter(status=int(action))
    orderStatus = order_status[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        orderStatus = 'All'
    param = {"order":order,'orderStatus':orderStatus }
    return render(request,'manage_order.html',param)

def delete_order(request,id):
    
    Booking.objects.get(id=id).delete()
    return manage_order(request)

def admin_order_track(request,pid):
    order = Booking.objects.get(id=pid)
    orderStatus = order_status
    status = int(request.GET.get('status',0))
    if status:
        order.status = status
        order.save()
        return redirect('admin_order_track', pid)
    param ={"order":order," orderStatus ": orderStatus }
    return render(request, 'admin-order-track.html', param) 

def admin_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = order_status
    status = int(request.GET.get('status',0))
    if status:
        order.status = status
        order.save()
        return redirect('admin_order_track', pid)
    return render(request, 'admin-order-track.html', locals()) 

from django.shortcuts import render
from .models import User, Profile

def manage_user(request):
    
    users = User.objects.all()

    param = {"users": users}
    return render(request, 'manage_user.html', param)

def delete_user(request):
    id = request.GET.get('id')
    User.objects.get(id=id).delete()
    return manage_user(request)

def admin_change_password(request):
    return render(request,"admin_change_password.html")

def admin_change_password_data(request):
    if request.method == 'POST':
        o = request.POST.get('o')
        n = request.POST.get('o')
        c = request.POST.get('o')
        user = authenticate(username=request.user.username,password=o)
        if user:
            if n == c:
                user.set_password(n)
                return admin_dashboard(request)
            else:
                param = {"msg":"Password did not match.."}
                return render(request,'admin_change_password.html',param)
        else:
            param = {"msg":"Credentials did not match.."}
            return render(request,'admin_change_password.html',param)
    else:
        param = {"msg":"Please fill the details"}
        return render(request,'admin_change_password.html',param)
    
def admin_dashboard(request):
    user = User.objects.all()
    category = Category.objects.all()
    product = Product.objects.all()
    new_order = Booking.objects.filter(status=1)
    dispatch_order = Booking.objects.filter(status=3)
    way_order = Booking.objects.filter(status=4)
    deliver_order = Booking.objects.filter(status=5)
    cancel_order = Booking.objects.filter(status=6)
    return_order = Booking.objects.filter(status=7)
    order = Booking.objects.filter()
    read_feedback = Feedback.objects.filter(status=1)
    unread_feedback = Feedback.objects.filter(status=2)
    return render(request,'admin_home.html',locals())

def admin_logout(request):
    logout(request)
    return render(request,'admin_login.html')


    




                
        



        


    
