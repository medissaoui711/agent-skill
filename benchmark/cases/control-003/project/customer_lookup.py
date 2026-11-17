from django.db import connection

def find_customer_by_email(email: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, email, display_name FROM customers WHERE email = %s",
            [email],
        )
        row = cursor.fetchone()

    if row is None:
        return None
    return {"id": row[0], "email": row[1], "display_name": row[2]}
