from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now as now_local

from .utils import validators
from .utils import fields


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Название карты', max_length=200)
    owner = fields.CardOwnerField(
        verbose_name='Владелец', max_length=200, validators=[validators.CardOwnerValidator]
    )
    pan = fields.CardNumberField(
        verbose_name='Номер карты', max_length=16, validators=[validators.CardNumberValidator]
    )
    expired_date = fields.ValidThruField(
        verbose_name='Срок истечения', max_length=10, validators=[validators.ValidThruValidator]
    )
    balance = models.DecimalField(verbose_name='Баланс', max_digits=30, decimal_places=2)

    class Meta:
        verbose_name = 'Карты'
        verbose_name_plural = 'Карты'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    date = models.DateTimeField(verbose_name='Дата операции', default=now_local)
    sum = models.DecimalField(verbose_name='Сумма', max_digits=30, decimal_places=2)
    OPERATION_TYPE_CHOICES = (
        ('income', 'доход'),
        ('expense', 'расход'),
    )
    operation_type = models.CharField(verbose_name='Тип операции', max_length=50, choices=OPERATION_TYPE_CHOICES)
    contr_agent = models.CharField(verbose_name='Контрагент', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'
        ordering = ['-date']
