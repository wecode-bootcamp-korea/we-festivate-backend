from .models.event_models import EventPost
from .models.building_models import Building
from django.views import View
from django.http import JsonResponse,HttpResponse
from datetime import datetime
from django.utils.dateformat import DateFormat
from urllib import parse
import json
POST_NUM = 8
def event_test(request):
    return HttpResponse("<h1>테스트</h1>")

class NewestView(View):
    def get(self, request):
        post_num = int(request.GET.get('num',POST_NUM))
        event_list = list(EventPost.objects.order_by('created_at').select_related('building').values('id','title','photo_url','date','max_rsvp','current_rsvp','building__name')[:post_num])
        return JsonResponse(event_list, safe=False)

class PriorityView(View):
    def get(self, request):
        post_num = int(request.GET.get('num',POST_NUM))
        todayStr = str(DateFormat(datetime.now()).format("ymd"))
        event_list = list(EventPost.objects.filter(date=todayStr).select_related('building').values('id','title','photo_url','date','max_rsvp','current_rsvp','building__name')[:post_num])
        return JsonResponse(event_list, safe=False)

class AllView(View):
    def get(self,request):
        start_id = int(request.GET.get('start',0))
        end_id = int(request.GET.get('end',POST_NUM))
        event_list = list(EventPost.objects.order_by('id').select_related('building').values('id','title','photo_url','date','max_rsvp','current_rsvp','building__name')[start_id:end_id])
        return JsonResponse(event_list, safe=False)

def search(request):
    return HttpResponse("<h1>검색 조건에 맞는 이벤트를 전달합니다! </h1>")

class DetailView(View):
    def get(self, request, event_id):
        print(f"event_id == {event_id}")
        event = EventPost.objects.get(pk=event_id)
        building =Building.objects.get(pk=event.building_id)
        print(building.name)
        # json_event = json.dumps(event)
        #building_list = list(Building.objects.filter(pk= 1).values('id'))
        #print(f"building_id == {event_list[0][id]}")
        return JsonResponse ({
            'event_id': event.id,
            'title': event.title,
            #빌딩 이름
            'building': building.name,
            'place': event.place,
            'date': event.date,
            'start_time': event.start_time,
            'end_time': event.end_time,
            'max_rsvp': event.max_rsvp,
            'current_rsvp': event.current_rsvp,
            'event_page_url': event.event_page_url,
            'main_text': event.main_text,
            'create_at': event.created_at,
            'updated_at': event.updated_at,
            'event_host_id': event.event_host_id,
            'photo_url': event.photo_url,
            #빌딩 세부 정보
            'contact': building.contact,
            'address': building.address,
            'latitude': building.latitude,
            'longitude': building.longitude
        }, safe=False)
