from django.urls import include, path
from rest_framework import routers

from .views import ProductViewSet, login

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")

urlpatterns = [
    path("login/", login, name="login"),
    path("", include(router.urls)),
]