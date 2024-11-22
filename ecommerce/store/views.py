from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.models import User, Order, CartItem
from store.serializers import UserSerializer, OrderSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from uuid import UUID

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id=None):
        if user_id:
            try:
                user = User.objects.get(id=user_id, is_superuser=False)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found or is a superuser"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = UserSerializer(user)
            return Response(serializer.data)
        
        users = User.objects.filter(is_superuser=False)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class OrderView(APIView):
    def get(self, request, order_id=None):
        try:
            if order_id:
                order = Order.objects.get(id=order_id)
                serializer = OrderSerializer(order)
                return Response(serializer.data)
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            order = Order.objects.get(id=request.data['id'])
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request):
        try:
            order = Order.objects.get(id=request.data['id'])
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.all()
        
        if cart_items:
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data)
        return Response({"error": "No cart items found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        cart_item = CartItem.objects.get(id=request.data['id'])
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            cart_item = CartItem.objects.get(id=request.data['id'])
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

class CheckoutView(APIView):
    def post(self, request):
        order = Order.objects.filter(user=request.user, status='Pending').first()

        if not order:
            return Response({"error": "No pending order found."}, status=status.HTTP_400_BAD_REQUEST)
            
        if order.cart_items.count() == 0:
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'Processed'
        order.save()
        return Response({"message": "Order processed successfully."}, status=status.HTTP_200_OK)

    def put(self, request):
        order = Order.objects.filter(user=request.user, status='Pending').first()
        if order:
            order.status = 'Processed' 
            order.save()
            return Response({"message": "Order processed successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "No pending order found."}, status=status.HTTP_400_BAD_REQUEST)



