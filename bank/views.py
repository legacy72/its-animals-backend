from django.utils import timezone
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from url_filter.integrations.drf import DjangoFilterBackend

from .models import (
    User, Card, Transaction,
)
from .serializers import (
    UserSerializer, CardSerializer, TransactionSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюшка для регистрации пользователей
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        """
        NOTE: Вьюшка используется только для создания, просматривать информацию о пользователях не нужно
        """
        return Response([], status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CardViewSet(viewsets.ModelViewSet):
    """
    Вьюшка для CRUD'a карт текущего пользователя
    """
    serializer_class = CardSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_fields = ['id', 'user', 'name', 'balance', ]

    def get_queryset(self):
        user = self.request.user
        queryset = Card.objects\
            .filter(user=user)\
            .prefetch_related('user')
        return queryset


class TransactionViewSet(viewsets.ModelViewSet):
    """
    Вьюшка для CRUD'a транзакций
    """
    serializer_class = TransactionSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_fields = ['id', 'user', 'card', 'sum', 'operation_type']

    def get_queryset(self):
        user = self.request.user.id
        queryset = Transaction.objects\
            .select_related('card')\
            .filter(user=user, card__user=user)\
            .order_by('date')
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            card = Card.objects.get(id=data['card'].id)
        except Card.DoesNotExist:
            return Response('Нет такой карты', status=status.HTTP_400_BAD_REQUEST)

        if data['operation_type'] == 'income':
            card.balance += data['sum']
        elif data['operation_type'] == 'expense':
            card.balance -= data['sum']
        card.save()

        serializer.save()
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
