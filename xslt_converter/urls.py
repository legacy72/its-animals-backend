from .views import *
from rest_framework import routers

router = routers.SimpleRouter()


router.register('converter', ConverterViewSet, basename='converter')
