from .models.event_models import EventPost
from .models.building_models import Building
from django.views import View
from django.http import JsonResponse,HttpResponse

def event_test(request):
    return HttpResponse("<h1>테스트</h1>")

def newest(request):
    event_list = list(EventPost.objects.order_by('create_at').values('id','title','building_id','photo_url','date','max_rsvp','max_rsvp')[:9])
    return JsonResponse(event_list, safe=False)

# def newest(request):
#     event_list = EventPost.objects.filter(pk=1)
#     event = event_list[0]
#     return JsonResponse({
#         'title': event.title,
#         'building_name':event.building_id,
#         'image':event.photo_url,
#         'date':event.date,
#         'max_rsvp':event.max_rsvp,
#         'max_rsvp':event.current_rsvp,
#     })

def priority(request):
    event_list = list(EventPost.objects.order_by('create_at').values('title','building_id','photo_url','date','max_rsvp','max_rsvp')[:9])
    return JsonResponse(event_list, safe=False)

def all(request):
    event_list = list(EventPost.objects.order_by('create_at').values('title','building_id','photo_url','date','max_rsvp','max_rsvp'))
    return JsonResponse(event_list, safe=False)

def search(request):
    return HttpResponse("<h1>검색 조건에 맞는 이벤트를 전달합니다! </h1>")

class DetailView(View):
    def get(self, request, event_id):
        print(f"event_id == {event_id}")
        event_list = list(EventPost.objects.filter(pk= event_id).values())
        #building_list = list(Building.objects.filter(pk= 1).values('id'))
        #print(f"building_id == {event_list[0][id]}")
        if len(event_list) == 0:
            return HttpResponse(status = 400)
        event = event_list[0]
        return JsonResponse (event_list, safe=False)
