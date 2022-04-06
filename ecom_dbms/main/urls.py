from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_view, name="product_page"),
    path("products/<str:pk>", views.product_detail, name="product_detail"),
    path("cart/", views.the_cart, name="cart_page"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("customer/", views.customer_view, name="customer"),
]
# just the name of the page
