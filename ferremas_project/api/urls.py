from django.urls import path
from .views import ProductListCreate, ProductRetrieveUpdateDestroy, PriceListCreate, PriceRetrieveUpdateDestroy, product_list_json, product_list_page, update_usd_prices, register, login_view, logout_view, cart_view

urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroy.as_view(), name='product-detail'),
    path('prices/', PriceListCreate.as_view(), name='price-list'),
    path('prices/<int:pk>/', PriceRetrieveUpdateDestroy.as_view(), name='price-detail'),
    path('products/json/', product_list_json, name='product-list-json'),
    path('products/list/', product_list_page, name='product-list-page'),  
    path('update-usd-prices/', update_usd_prices, name='update_usd_prices'),  
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cart/', cart_view, name='cart'),
]
