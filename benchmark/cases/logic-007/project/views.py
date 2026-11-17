from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

PAGE_SIZE = 20

@login_required
def customer_page(request):
    queryset = Customer.objects.order_by("id")
    page_number = max(int(request.GET.get("page", "1")), 1)
    start = page_number * PAGE_SIZE
    end = start + PAGE_SIZE
    customers = list(queryset[start:end].values("id", "name"))
    return JsonResponse({"page": page_number, "customers": customers})
