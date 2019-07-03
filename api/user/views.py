from django.http import HttpResponse, JsonResponse
from django.views import View #why??

def testing(request):
    return HttpResponse("<h1>장고 넌 죽었어 우리한테 </h1>")
