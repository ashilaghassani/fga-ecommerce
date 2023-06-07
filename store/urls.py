from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.home, name="home"),
    
	path('store/', views.store, name="store"),
    path('product/<pid>', views.product_detail, name="product_detail"),
    path('contact/', views.contact, name="contact"),
    
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    
	path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

]