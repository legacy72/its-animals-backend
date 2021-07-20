from rest_framework import routers

from .views import *


router = routers.DefaultRouter()

router.register('cards', CardViewSet, basename='cards')
router.register('transactions', TransactionViewSet, basename='transactions')
router.register('registration', UserViewSet, basename='registration')
