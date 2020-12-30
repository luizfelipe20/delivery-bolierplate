from rest_framework import routers
from platform_delivery.api import *


router = routers.DefaultRouter(trailing_slash=True)
router.register(r'user',UserViewSet)
router.register(r'category',CategoryViewSet)
router.register(r'orders',OrderViewSet)
router.register(r'bag',BagViewSet)
router.register(r'product',ProductViewSet)
router.register(r'favorite',FavoriteViewSet)
router.register(r'address',AddressViewSet)
router.register(r'rating',RatingViewSet)
