import xmltodict
import lxml.etree as ET
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Converter
from .serializers import ConverterSerializer
from .utils.price_converter import price_to_text


class ConverterViewSet(viewsets.ModelViewSet):
    queryset = Converter.objects.all()
    serializer_class = ConverterSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_xml = request.FILES['file_xml']
        file_xslt = request.FILES['file_xslt']

        dom = ET.parse(file_xml)
        xslt = ET.parse(file_xslt)

        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        dict = xmltodict.parse(newdom)
        data = dict['HTML']['BODY']['TABLE'].get('TR', 'TH')
        res = []
        for d in data:
            res.append({
                'name': d['TD'][0],
                'author': d['TD'][1],
                'text_price': price_to_text(d['TD'][2]),
            })

        return Response(
            res,
            status=status.HTTP_200_OK,
        )
