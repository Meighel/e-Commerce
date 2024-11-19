from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.models import User, Order, CartItem
from store.serializers import UserSerializer, OrderSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated

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
        if order_id:
            order = Order.objects.get(id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def put(self, request):
        order = Order.objects.get(id=request.data['id'])
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        order = Order.objects.get(id=request.data['id'])
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not isinstance(request.user, User):
            return Response({"error": "User not found or not authenticated."}, status=status.HTTP_400_BAD_REQUEST)

        pending_order = Order.objects.filter(user=request.user, status='Pending').first()
        if pending_order:
            cart_items = pending_order.cart_items.all()
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data)
        return Response({"error": "No pending order found."}, status=status.HTTP_404_NOT_FOUND)

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
        cart_item = CartItem.objects.get(id=request.data['id'])
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CheckoutView(APIView):
    def post(self, request):
        order = Order.objects.filter(user=request.user, status='Pending').first()
        if order:
            order.status = 'Processed'
            order.save()
            return Response({"message": "Order processed successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "No pending order found."}, status=status.HTTP_400_BAD_REQUEST)
