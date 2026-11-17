from django.db import connection
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def search_customers(request):
    term = request.GET.get("q", "")
    sql = (
        "SELECT id, display_name FROM customers "
        f"WHERE display_name ILIKE '%{term}%' "
        "ORDER BY display_name"
    )
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

    return JsonResponse({
        "results": [{"id": row[0], "name": row[1]} for row in rows]
    })
