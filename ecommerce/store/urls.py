from django.urls import path, include
from store.views import UserView, OrderView, CartItemView, CheckoutView

urlpatterns = [
    path('users/', UserView.as_view(), name='user-create'),
    path('users/<uuid:user_id>/', UserView.as_view(), name='user-detail'),
    path('orders/', OrderView.as_view(), name='order-list'),
    path('orders/<uuid:order_id>/', OrderView.as_view(), name='order-detail'),
    path('orders/<uuid:order_id>/checkout', CheckoutView.as_view(), name='checkout'),
    path('cart-items/', CartItemView.as_view(), name='cart-item'),
    path('cart-items/<uuid:cart_item_id>/', CartItemView.as_view(), name='cart-item-detail'),
]
