from django.http import HttpResponse, JsonResponse

def event_test(request):
    return HttpResponse("<h1>우리 어벤저스가 잡으러 간다 </h1>")



