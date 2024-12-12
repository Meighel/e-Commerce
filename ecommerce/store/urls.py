from django.urls import path, include
from store.views import UserListCreateView, UserDetailView, OrderListCreateView, OrderDetailView, CartItemListView, CartItemDetailView, CheckoutView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<uuid:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<uuid:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<uuid:order_id>/checkout', CheckoutView.as_view(), name='checkout'),
    path('cart-items/', CartItemListView.as_view(), name='cart-item-list'), 
    path('cart-items/<uuid:cart_item_id>/', CartItemDetailView.as_view(), name='cart-item-detail'), 
]
