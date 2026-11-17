from django.db.models import Count, Q
from .models import Customer


def list_customers():
    customers = Customer.objects.order_by("id")[:100]
    results = []
    for customer in customers:
        open_orders = customer.orders.filter(status="open").count()
        results.append({
            "id": customer.id,
            "name": customer.display_name,
            "open_order_count": open_orders,
        })
    return results
