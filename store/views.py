from  django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from .forms import CreateUserForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required  

from django_ratelimit.decorators import ratelimit



import json
import datetime

# Create your views here.

def home(request):
    context ={}
    return render(request,'store/home.html',context)

def registerPage(request):
    form = CreateUserForm()

    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Your account has been successfully created , ' + user +'!')

            return redirect('login')
        
    context ={'form':form}
    return render(request,'store/register.html',context)

@ratelimit(key='user', rate='5/m', method=['POST'])
def loginPage(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
       
        
    context ={}
    return render(request,'store/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def contact(request):

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        data = Contact(name=name,email=email, message=message)
        data.save()
        context = {'form_created': True}
        return render(request, 'store/contact.html',context)
    else:
        return render(request,'store/contact.html')


# store = ngembaliin list produk
def store(request):
    # ambil produk dari database
    ordering = request.GET.get('ordering', "")  
    category_filter = request.GET.getlist('category')

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()

    if ordering:
        products = products.order_by(ordering) 
    if category_filter:
        products = products.filter(kategori__in=category_filter)
  
  

    context = {'products':products, 'cartItems': cartItems, 'selected_categories': category_filter}
    return render(request,'store/store.html',context)

def product_detail(request,pid):
    
    product = Product.objects.get(pid=pid) 
    additional_images = product.additional_images.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all
        cartItems = order.get_cart_items
        order_items = OrderItem.objects.filter(product=product, order=order)
        productItem = sum(item.quantity for item in order_items)
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'get_product_item':0,'shipping':False}
        cartItems = order['get_cart_items']
        productItem = 0

    context = {'product':product, 'cartItems': cartItems, 'productItem':productItem, 'additional_images': additional_images}
    
    return render(request,'store/product_detail.html',context)

@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        cartItems = order['get_cart_items']
    context ={'items':items, 'order':order, 'cartItems': cartItems}

    return render(request,'store/cart.html',context)


@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']
    context ={'items':items, 'order':order, 'cartItems': cartItems}

    return render(request,'store/checkout.html',context)



@login_required(login_url='login')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
 
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('udh di update', safe=False)

@login_required(login_url='login')
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp() 
    data = json.loads(request.body)
    
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id


        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
		    )

    else:
        print('ga login')
        # customer, order = guestOrder(request, data)

    return JsonResponse('Payment Completeed',safe=False)