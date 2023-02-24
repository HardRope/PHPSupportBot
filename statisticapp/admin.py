from django.contrib import admin
from django.db.models import Avg, Count, Sum

from statisticapp.models import OrderSummary

@admin.register(OrderSummary)
class OrderSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/order_summary_change_list.html'
    date_hierarchy = 'created_at'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        metrics = {
            'total': Count('id'),
            'total_sales': Sum('subscription__tariff__price'),
        }
        response.context_data['summary'] = list(
            qs
            .values('subscription__client__user__tg_chat_id')
            .annotate(**metrics)
            .order_by('-total_sales')
        )
        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )
        return response
