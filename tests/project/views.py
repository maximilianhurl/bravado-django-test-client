from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


def get_params_view(request):
    return JsonResponse({
        "paramInt": int(request.GET.get('paramInt', None)),
        "paramString": request.GET.get('paramString', None)
    })


cat_1 = {
    "id": "1",
    "name": "Tar tar sauce",
    "color": "Brown",
    "age": 1,
    "friends": [],
}

cat_2 = {
    "id": "2",
    "name": "Minky",
    "color": "White",
    "age": 2,
    "friends": [cat_1],
}

cat_3 = {
    "id": "3",
    "name": "Minky",
    "color": "White",
    "age": 1,
    "friends": [],
}


@api_view(['GET', 'POST'])
def cats_list(request):
    if request.method == 'POST':
        return Response(request.data, status=201)
    return Response({
        "count": None,
        "CAT_HEADER": request.META.get('CAT_HEADER', None),
        "results": [cat_1, cat_2, cat_3]
    }, status=200)


@api_view(['PUT'])
def cat_update(request, cat_name):
    return Response({
        **request.data,
        "name": cat_name,
    }, status=200)
