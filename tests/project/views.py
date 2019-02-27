from django.http import JsonResponse


def get_params_view(request):
    return JsonResponse({
        "paramInt": int(request.GET.get('paramInt', None)),
        "paramString": request.GET.get('paramString', None)
    })
