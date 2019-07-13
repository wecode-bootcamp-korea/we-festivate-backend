from .models.event_models import EventPost, EventRsvp, EventComment
from user.models import User, UserType
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

    def post(self, request, event_id):
        page_user = json.loads(request.body)
        user1 = User.objects.get(user_id=page_user["user_id"])
        print(user1.id)

        if EventRsvp.objects.filter(user_id=user1).exists():
            rsvp_result = True
        else :
            rsvp_result = False

        event = EventPost.objects.get(pk=event_id)
        building =Building.objects.get(pk=event.building_id)
        event_comment1 = list(EventComment.objects.filter(event_id=event_id).prefetch_related('user').values())

        return JsonResponse ({
            "event_id": event.id,
            "title": event.title,
            #빌딩 이름
            "building": building.name,
            "place": event.place,
            "date": event.date,
            "start_time": event.start_time,
            "end_time": event.end_time,
            "max_rsvp": event.max_rsvp,
            "current_rsvp": event.current_rsvp,
            "event_page_url": event.event_page_url,
            "main_text": event.main_text,
            "create_at": event.created_at,
            "updated_at": event.updated_at,
            "event_host_id": event.event_host_id,
            "photo_url": event.photo_url,
            #빌딩 세부 정보
            "contact": building.contact,
            "address": building.address,
            "latitude": building.latitude,
            "longitude": building.longitude,
            "rsvp_result": rsvp_result,
            "event_comment": event_comment1
        }, safe=False)

class RsvpView(View):

    def post(self, request, event_id):
        page_user = json.loads(request.body)
        user1 = User.objects.get(user_id=page_user["user_id"])
        rsvp_event = EventPost.objects.get(id=event_id)

        if EventRsvp.objects.filter(user_id=user1.id, event_id=event_id).exists(): #user_id는 integer 값으로 user테이블의 pk와 동일
            rsvp_result = False
            rsvp_message = '이미 신청한 이벤트 입니다.'
        elif rsvp_event.current_rsvp >= rsvp_event.max_rsvp: #추후 개선 필요
            rsvp_result = False
            rsvp_message = '이벤트 신청이 완료 되었습니다. 댓글을 남겨주시면 대기자 명단 처리 하겠습니다.'
        else :
            rsvp_event.current_rsvp += 1
            rsvp_event.save()
            EventRsvp.objects.create(event_id=event_id, user_id=user1.id)
            rsvp_result = True
            rsvp_message = '이벤트 신청이 정상 처리되었습니다.'

        return JsonResponse ({
            "current_rsvp": rsvp_event.current_rsvp,
            "rsvp_result": rsvp_result,
            "rsvp_message": rsvp_message
        }, safe=False)

class CommentView(View):

    def post(self, request, event_id):
        comment_data = json.loads(request.body)
        user1 = User.objects.get(user_id=comment_data["user_id"])
        EventComment.objects.create(event_id=event_id, user_id=user1.user_id, comment_text=comment_data["comment_text"])
        comment_result = True
        comment_message = "님, 댓글이 정상적으로 등록되었습니다."

        return JsonResponse ({
            "user_id": user1.user_id,
            "comment_result": True,
            "comment_message": comment_message
        }, safe=False)

class NewEventView(View):

    def post(self, request):

        new_event = json.loads(request.body)
        user1 = User.objects.get(user_id=new_event["user_id"])

        EventPost.objects.create(title=new_event["title"], building=new_event["building_id"], place=new_event["place"],date=new_event["date"], start_time=new_event["start_time"], end_time=new_event["end_time"],max_rsvp=new_event["max_rsvp"],event_page_url=new_event["event_page_url"],main_text=new_event["main_text"],photo_url=new_event["photo_url"],event_host=user1.id)
        message="이벤트가 정상적으로 등록되었습니다."

        return JsonResponse({
            "result_message": message
        })