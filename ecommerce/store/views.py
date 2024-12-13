from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.models import User, Order, CartItem
from store.serializers import UserSerializer, OrderSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from uuid import UUID
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

class UserListCreateView(APIView):

    permission_classes = [AllowAny] 

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=UserSerializer,
        responses={201: UserSerializer(), 400: 'Invalid data'}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="List all users",
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetailView(APIView):

    permission_classes = [AllowAny] 

    @swagger_auto_schema(
        operation_description="Retrieve user information",
        responses={200: UserSerializer(), 404: 'User not found'}
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all orders",
        responses={200: OrderSerializer(many=True), 401: 'Unauthorized'}
    )
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new order",
        request_body=OrderSerializer,
        responses={201: OrderSerializer(), 400: "Invalid data", 401: 'Unauthorized'}
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete all orders",
        responses={
            200: "All orders deleted successfully",
            401: 'Unauthorized'
        }
    )
    def delete(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        deleted_count, _ = Order.objects.all().delete()
        return Response(
            {"message": f"All orders ({deleted_count}) deleted successfully."},
            status=status.HTTP_200_OK,  # Using 200 OK to include a response body
        )

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get details of an order by its ID",
        responses={200: OrderSerializer(), 404: 'Order not found', 401: 'Unauthorized'}
    )
    def get(self, request, order_id):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an order status or details",
        request_body=OrderSerializer,
        responses={200: OrderSerializer(), 400: "Bad request", 404: "Order not found", 401: 'Unauthorized'}
    )
    def put(self, request, order_id):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete an order by its ID",
        responses={
            200: "Order deleted successfully",
            404: "Order not found",
            401: 'Unauthorized'
        }
    )
    def delete(self, request, order_id):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return Response(
                {"message": f"Order with ID {order_id} deleted successfully."},
                status=status.HTTP_200_OK,  # Using 200 OK to include a response body
            )
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

class CartItemListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all cart items",
        responses={200: CartItemSerializer(many=True), 404: 'No cart items found', 401: 'Unauthorized'}
    )
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        cart_items = CartItem.objects.all()
        if cart_items.exists():
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data)
        return Response({"error": "No cart items found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Create a new cart item",
        request_body=CartItemSerializer,
        responses={201: CartItemSerializer(), 400: 'Invalid data', 401: 'Unauthorized'}
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete all cart items",
        responses={200: 'All cart items deleted', 401: 'Unauthorized'}
    )
    def delete(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        deleted_count, _ = CartItem.objects.all().delete()
        return Response(
            {"message": f"All cart items ({deleted_count}) deleted successfully."},
            status=status.HTTP_200_OK,
        )

class CartItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a specific cart item by ID",
        responses={200: CartItemSerializer(), 404: 'Cart item not found', 401: 'Unauthorized'}
    )
    def get(self, request, cart_item_id=None):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if cart_item_id:
            try:
                cart_item = CartItem.objects.get(id=cart_item_id)
                serializer = CartItemSerializer(cart_item)
                return Response(serializer.data)
            except CartItem.DoesNotExist:
                return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Cart item ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a specific cart item by ID",
        responses={200: CartItemSerializer(), 400: "Invalid data", 404: "Cart item not found", 401: 'Unauthorized'},
        request_body=CartItemSerializer
    )
    def put(self, request, cart_item_id=None):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if cart_item_id:
            try:
                cart_item = CartItem.objects.get(id=cart_item_id)
                serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except CartItem.DoesNotExist:
                return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Cart item ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific cart item",
        responses={204: 'Cart item deleted', 404: 'Cart item not found', 401: 'Unauthorized'}
    )
    def delete(self, request, cart_item_id=None):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart_item.delete()
            return Response({"message": f"Cart item with ID {cart_item_id} deleted successfully."})
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Process an order by changing its status to 'Processed'",
        responses={200: 'Order processed successfully', 400: 'Invalid order status', 404: 'Order not found', 401: 'Unauthorized'}
    )
    def put(self, request, order_id):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if order.status == 'Pending':
            order.status = 'Processed'
            order.save()
            return Response({"message": "Order processed successfully."}, status=status.HTTP_200_OK)
        elif order.status == 'Processed':
            return Response({"message": "Order has already been processed."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid order status."}, status=status.HTTP_400_BAD_REQUEST)