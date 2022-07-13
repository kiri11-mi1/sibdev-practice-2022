from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, BEFORE_SAVE

from .managers import TransactionManager
from ..constants import TransactionTypes


class Transaction(LifecycleModelMixin, models.Model):
    transaction_type = models.CharField(
        max_length=7,
        choices=TransactionTypes.CHOICES,
        verbose_name='Тип операции',
    )
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Пользователь',
    )
    category = models.ForeignKey(
        to='pockets.TransactionCategory',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Категория',
        null=True,
        blank=True,
    )
    transaction_date = models.DateField(
        verbose_name='Дата операции',
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма операции',
        validators=(MinValueValidator(Decimal('0.01')),),
    )

    objects = TransactionManager()

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'

    def __str__(self) -> str:
        return f'{self.amount} {TransactionTypes.CHOICES_DICT[self.transaction_type]}'

    @hook(BEFORE_SAVE, when='category')
    def validate_transaction_by_type(self):
        if self.transaction_type == TransactionTypes.INCOME:
            self.category = None
