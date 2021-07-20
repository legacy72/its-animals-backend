"""hackaton URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from bulling_analysis.urls import router as bulling_router
from check_vulnerability.urls import router as vulnerability_router
from email_validator.urls import router as email_validator_router
from xslt_converter.urls import router as xslt_converter_router
from bank.urls import router as bank_router
from decryptor.urls import router as decryptor_router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('bulling/', include(bulling_router.urls)),
    path('vulnerability/', include(vulnerability_router.urls)),
    path('email_validator/', include(email_validator_router.urls)),
    path('xslt_converter/', include(xslt_converter_router.urls)),
    path('bank/', include(bank_router.urls)),
    path('decryptor/', include(decryptor_router.urls))
]
