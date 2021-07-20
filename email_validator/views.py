from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from .services import *
from rest_framework import status
from rest_framework.response import Response


class EmailValidationViewSet(ViewSet):
    def create(self, request):
        email_to_validate = request.data["email"]

        is_valid_format(email_to_validate)
        domain = get_domain(email_to_validate)
        mxRecord = mx_lookup(domain)
        smtp_response = get_smpt_response(
            mxRecord=mxRecord,
            fromAddress="random@yandex.ru",
            addressToVerify=email_to_validate,
        )
        result = {
            'domain': domain,
            'mail_exchanger': mxRecord,
            'smtp_response': smtp_response,
        }
        return Response(result, status=status.HTTP_200_OK)
