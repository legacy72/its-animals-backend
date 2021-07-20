from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from url_filter.integrations.drf import DjangoFilterBackend
from rest_framework.decorators import action
from .models import MD5Rainbow
from .serializers import MD5RainbowSerializer
import base64
import re
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


class MD5RainbowViewSet(viewsets.ModelViewSet):
    serializer_class = MD5RainbowSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]

    @action(detail=False, methods=["post"])
    def upload_wordlist(self, request):
        wordlist = request.data["wordlist"]
        wordlist_dict = {}
        # with open(wordlist) as f:
        for line in wordlist:
            (hash_value, key) = line.split()
            wordlist_dict[hash_value.decode("utf-8")] = key.decode("utf-8")
        try: 
            objs = [
                MD5Rainbow(hash_value=hash_value, key=key) for hash_value, key in wordlist_dict.items()
            ]
        except ValueError:
            print(wordlist_dict)

        MD5Rainbow.objects.bulk_create(objs)
        return Response('ok', status=status.HTTP_200_OK)


class DecryptorViewSet(viewsets.ViewSet):
    BASE64REGEX = r'^((?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)$'

    def create(self, request):
        to_decrypt = request.data["to_decrypt"]
        if re.match(self.BASE64REGEX, to_decrypt):
            try:
                decrypted_value = self.decrypt_base64(to_decrypt)
                result = {
                    'encryption_method': 'base64',
                    'decrypted_value': decrypted_value.decode("utf-8")
                }
                return Response(result, status=status.HTTP_200_OK)
            except Exception:
                pass
        if self.is_ascii_code(to_decrypt):
            decrypted_value = self.decrypt_ascii_code(to_decrypt)
            result = {
                'encryption_method': 'ascii code',
                'decrypted_value': decrypted_value
            }
            return Response(result, status=status.HTTP_200_OK)

        try:
            rainbow_obj = MD5Rainbow.objects.get(hash_value=to_decrypt)
            result = {
                'encryption_method': 'md5',
                'decrypted_value': rainbow_obj.key
            }
            return Response(result, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response('Decryption failed ', status=status.HTTP_400_BAD_REQUEST)
                 


    def is_ascii_code(self, s):
        return all([c.isdigit() or c == ' ' for c in s])

    def decrypt_base64(self, s):
        decrypted_value = base64.b64decode(s)
        if base64.b64encode(decrypted_value).decode("utf-8") == s:
            return decrypted_value
    
    def decrypt_ascii_code(self, s):
        data_to_list = s.replace(' ', ',').split(',')
        ascii_list = [int(num) for num in data_to_list]
        decrypted_value = ''.join(map(chr, ascii_list))

        if list(map(ord, decrypted_value)) == ascii_list:
            return decrypted_value