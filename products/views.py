from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=["GET"], url_path="low-stock")
    def low_stock(self, request):
        low_stock_products = Product.objects.filter(quantity__lte=5)
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

