from django.urls import path
from . import views

# viewtwo
from . import viewstwo

urlpatterns = [
    path('', views.index, name="index"),
    path('collections', views.collections, name="collections"),
    path('collections/<str:slug>', views.collectionsview, name="collectionsview"),
    path('collections/<str:cate_slug>/<str:prod_slug>', views.productview, name='productview'),

    # auth
    path('register', views.register, name="register"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),


    path('add-to-cart',views.add_to_cart, name="add-to-cart"),
    path('cart', views.cart, name="cart"),
    path('updateCart', views.updateCart, name="updateCart"),
    path('deleteCartItem', views.deleteCartItem, name="deleteCartItem"),

    path('product-list', views.productlist, name="productlist"),
    path('searchproduct', views.searchproduct, name='searchproduct'),

    # from here use viewstwo.py file
    path('wishlist', viewstwo.wishlist, name="wishlist"),
    path('addingWishlist', viewstwo.addingWishlist, name="addingWishlist"),
    path('deleteWistItem', viewstwo.deleteWistItem, name='deleteWistItem'),

    path('checkout', viewstwo.checkout, name="checkout"),
    path('place-order', viewstwo.placeorder, name="placeorder"),
    path('proceed-to-pay', viewstwo.razerpay, name='razerpay'),

    path('my-order', viewstwo.orders, name='orders'),
    path('orderview/<str:t_no>',viewstwo.orderview, name="orderview")

]