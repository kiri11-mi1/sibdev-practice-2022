from django.contrib import admin

from ..models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'transaction_type', 'category', 'user', 'transaction_date')
    list_filter = ('transaction_type', 'transaction_date')
    search_fields = ('amount', 'category', 'user', 'transaction_date')
