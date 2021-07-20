from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('email_validator',
                EmailValidationViewSet,
                basename='email_validator')
