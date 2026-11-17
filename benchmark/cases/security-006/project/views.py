import base64
import pickle

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def import_report_state(request):
    encoded_state = request.POST["state"]
    raw_state = base64.b64decode(encoded_state)
    state = pickle.loads(raw_state)
    return JsonResponse({"columns": state.get("columns", [])})
