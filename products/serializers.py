from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    in_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_in_stock(self, obj):
        return obj.is_in_stock()