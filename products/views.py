from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

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
