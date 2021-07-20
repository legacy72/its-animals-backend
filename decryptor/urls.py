from rest_framework import routers
from .views import MD5RainbowViewSet, DecryptorViewSet

router = routers.DefaultRouter()
router.register('md5rainbow', MD5RainbowViewSet, basename='md5rainbow')
router.register('decryptor', DecryptorViewSet, basename='decryptor')