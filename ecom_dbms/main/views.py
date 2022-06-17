from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import json
import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, CustomerForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def product_view(request):
    productss = Product.objects.all()
    return render(request, "products/product_page.html", {"productss": productss})


# templates is the path so just add the other directory paths and go to urls

# product by ids; urls/id
# use filter instead of get as it gives a query set and not object
def product_detail(request, pk):
    prod_desc = Product.objects.filter(id=pk)
    return render(request, "products/product_detail.html", {"prod_desc": prod_desc})


# CART.JS
# Create your views here.
def the_cart(request):

    if request.user.is_authenticated:
        # One to oe relationship
        customer = request.user.customer
        # if not ordered, create one
        # Read docs
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # use the object 'order' not class 'order'
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        # fix for logout
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
        }  # fix for unauthenticated cart_page.html user, returns empty
        cartItems = order["get_cart_items"]

    products = Product.objects.all()
    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/cart_page.html", context)


def checkout(request):

    if request.user.is_authenticated:
        # One to one relationship
        customer = request.user.customer
        # if not ordered, create one
        # Read docs
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # use the object 'order' not class 'order'
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        # fix for logout
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
        }  # fix for unauthenticated cart_page.html user, returns empty
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order}
    return render(request, "store/checkout.html", context)


def updateItem(request):
    # logs items to backend
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    # print("Action:", action)
    # print("productId:", productId)

    # creates cutomer and order if not created

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # if item already exists in cart, dont create new item
    # only change quantity
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # if action is add, item is added to cart
    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    # if number of a particular item i <0, take it off the cart
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    # authentication
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data["form"]["total"])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping is True:
            Address.objects.create(
                customer=customer,
                order=order,
                house_No=data["shipping"]["house_No"],
                street=data["shipping"]["street"],
                locality=data["shipping"]["locality"],
                landmark=data["shipping"]["landmark"],
                city=data["shipping"]["city"],
                state=data["shipping"]["state"],
                zipcode=data["shipping"]["zipcode"],
            )

    else:
        print("User is logged in..")
    return JsonResponse("Payment complete", safe=False)


# Changed Usercreation form to newuserform
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        # if valid form
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            # specific user
            messages.success(request, f"New account created: {username} ")
            # login
            login(request, user)
            messages.info(request, f"You are now logged in as: {username}")
            return redirect("/customer")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    form = NewUserForm()
    return render(request, "authentication/register.html", context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")


# login csrf
@csrf_exempt
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)

        # if valid form
        if form.is_valid():
            # read more about cleaned dat
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # access, specify arguement name
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as: {username}")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password")

        # just return same error message
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(
        request=request,
        template_name="authentication/login.html",
        context={"form": form},
    )


def customer_view(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)

        if form.is_valid():
            customer = form.save()
            fname = form.cleaned_data.get("first_name")
            messages.success(request, f"Welcome: {fname} ")
            return redirect("/")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    form = CustomerForm()
    return render(request, "authentication/cust_details.html", context={"form": form})
