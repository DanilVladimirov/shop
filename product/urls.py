from django.urls import include, path
from product.views import *


urlpatterns = [
    path('shop/', shop_main_page, name='main_page'),
    path('shop/basket/', basket, name='basket_page'),
    path('shop/category/<int:pk>/', category_page, name='category_page'),
    path('shop/currency', select_curr, name='category_page'),
    path('shop/checkout/', checkout_page, name='checkout_page'),
    path('shop/invoice/<int:pk>/', get_invoice, name='invoice_page'),
    path('shop/invoice/<int:pk>/edit/', edit_invoice, name='invoice_edit_page'),
    path('shop/product/<int:pk>/', product_page_new, name='product_page'),
    path('shop/wishlist/', wishlist, name = 'wishlist'),
    path('shop/subeditprice/', subeditprice, name = 'subeditprice'),
]