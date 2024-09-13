from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product


@api_view(['GET', 'POST'])
def api_home(request, *args, **kwargs):
    # NOTE:- DRF Api
    instance = Product.objects.all().order_by("?").first()
    data = {}
    if instance:
        data = model_to_dict(instance, fields=['id', 'title', 'price'])
    return Response(data)


"""
NOTE:- Django API
def api_home(request, *args, **kwargs):
    # Serialization:- instance -> python dict --> JSON
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data = model_to_dict(model_data, fields=['id', 'title', 'price'])
        # data['price'] = float(data['price'])
        # json_data = json.dumps(data)
    return JsonResponse(data)
"""

"""
NOTE:- Django API

def api_home(request, *args, **kwargs):
    # request: django's HTTPRequest
    body = request.body  # byte string of JSON data
    # params = dict(request.GET)  # urls query params
    print(body)
    data = {}
    try:
        data = json.loads(body)
    except:
        pass
    data['params'] = dict(request.GET)
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type
    return JsonResponse(data)
"""
