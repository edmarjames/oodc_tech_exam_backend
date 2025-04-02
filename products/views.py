from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Product
from .serializers import ProductSerializer


@api_view(["POST"])
def login(request):

    username = request.data.get("username", None)
    password = request.data.get("password", None)

    user = authenticate(username=username.strip(), password=password.strip())

    if user is not None:
        if user.is_superuser:
            return Response({
                "message": "Login successful",
                "is_admin": True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Login failed",
                "is_admin": False
            }, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({
            "error": "Invalid username or password"
        }, status=status.HTTP_401_UNAUTHORIZED)


class ProductPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = "page_size"

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="low-stock")
    def low_stock(self, request):
        low_stock_products = Product.objects.filter(quantity__lte=5)
        page = self.paginate_queryset(low_stock_products)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["PATCH"], url_path="update-stock")
    def update_stock(self, request, pk=None):
        product = self.get_object()
        amount = request.data.get("amount", 0)
        action = request.query_params.get("action", None)

        if action.lower() not in ["increase", "decrease"]:
            return Response({
                "message": "Invalid action specified. Use 'increase' or 'decrease'."
            })

        if action.lower() == "increase":
            response = product.increase_stock(amount)
        if action.lower() == "decrease":
            response = product.reduce_stock(amount)

        if response["success"]:
            return Response({
                "message": response["message"],
                "data": ProductSerializer(product).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": f"Failed to {action} stock",
                "error": response["error"]
            }, status=status.HTTP_400_BAD_REQUEST)

