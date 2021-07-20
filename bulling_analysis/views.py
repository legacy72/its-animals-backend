from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .sentiment_analysis.predictions.predictor import Predictor


class BullingViewSet(viewsets.ViewSet):
    """
    METHOD: POST
    params: text - текст для проверки
    returns:
        {
            'probability_bad': насколько буллинг,
            'probability_normal': насколько норм,
            'bad_words': словарь буллинговых слов с процентом их отношения к уникальным словам,
        }
    """
    def create(self, request):
        text = self.request.data.get('text')
        predictor = Predictor()
        predictor.train_data()
        res = predictor.get_sentiment_percentage(text)
        return Response(res, status=status.HTTP_200_OK)
