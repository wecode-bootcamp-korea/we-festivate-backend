from .models.event_models import EventPost, EventRsvp, EventComment, EventLike
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
        event_list = list(EventPost.objects.order_by('-created_at').select_related('building').values('id','title','photo_url','date','max_rsvp','current_rsvp','building__name')[:post_num])
        return JsonResponse(event_list, safe=False)

class PriorityView(View):

    def get(self, request):
        post_num = int(request.GET.get('num',POST_NUM))
        todayStr = str(DateFormat(datetime.now()).format("ymd"))
        event_list = list(EventPost.objects.filter(date=todayStr).select_related('building').values(
            'id',
            'title',
            'photo_url',
            'date',
            'max_rsvp',
            'current_rsvp',
            'building__name')[:post_num])
        return JsonResponse(event_list, safe=False)

class AllView(View):

    def get(self,request):
        start_id = int(request.GET.get('start',0))
        end_id = int(request.GET.get('end',POST_NUM))
        event_list = list(EventPost.objects.order_by('-id').select_related('building').values(
            'id',
            'title',
            'photo_url',
            'date',
            'max_rsvp',
            'current_rsvp',
            'building__name')[start_id:end_id])
        return JsonResponse(event_list, safe=False)

class EventTitleSearchView(View):

    def post(self,request):
        query_string = json.loads(request.body)
        # title_q = request.GET.get('title_q','')

        if query_string["title_query"]:
            title_query_data = EventPost.objects.values().filter(title__icontains=query_string["title_query"])
        else:
            title_query_data = EventPost.objects.values().all()

        return JsonResponse(list(title_query_data), safe=False)

class EventDetailView(View):

    def post(self, request, event_id):
        page_user = json.loads(request.body)
        if page_user["login_state"]:
            user1 = User.objects.get(id=page_user["user_pk"])

            if EventRsvp.objects.filter(user_id=user1.id, event_id=event_id).exists():
                rsvp_result = True
            else :
                rsvp_result = False

            if EventLike.objects.filter(user_id=user1.id, event_id=event_id).exists():
                like_result = True
            else :
                like_result = False

        else:
            rsvp_result = False
            like_result = False

        event = EventPost.objects.get(pk=event_id)
        building =Building.objects.get(pk=event.building_id)
        event_comment = list(EventComment.objects.filter(event_id=event_id).prefetch_related('user').values(
            'user__name',
            'comment_text',
            'created_at'))

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
            "like_result": like_result,
            "event_comment": event_comment
        }, safe=False)

class RsvpView(View):

    def post(self, request, event_id):
        page_user = json.loads(request.body)
        user1 = User.objects.get(id=page_user["user_pk"])
        rsvp_event = EventPost.objects.get(id=event_id)

        if EventRsvp.objects.filter(user_id=user1.id, event_id=event_id).exists(): #user_id는 integer 값으로 user테이블의 pk와 동일
            rsvp_result = False
            rsvp_message = 'rsvp_reserved'
        elif rsvp_event.current_rsvp >= rsvp_event.max_rsvp: #추후 개선 필요
            rsvp_result = False
            rsvp_message = 'rsvp_overflow'
        else :
            rsvp_event.current_rsvp += 1
            rsvp_event.save()
            new_rsvp = EventRsvp.objects.create(event_id=event_id, user_id=user1.id)
            new_rsvp.save()
            rsvp_result = True
            rsvp_message = 'rsvp_success'

        return JsonResponse ({
            "current_rsvp": rsvp_event.current_rsvp,
            "rsvp_result": rsvp_result,
            "rsvp_message": rsvp_message
        }, safe=False)

class LikeView(View):

    def post(self, request, event_id):
        page_user = json.loads(request.body)
        user1 = User.objects.get(id=page_user["user_pk"])
        like_event = EventPost.objects.get(id=event_id)

        if EventLike.objects.filter(
            user_id=user1.id,
            event_id=event_id).exists():
            #user_id는 integer 값으로 user테이블의 pk와 동일
            like_result = False
            like_message = 'like_fail'
        else :
            like_event.like_num += 1
            like_event.save()
            new_like = EventLike.objects.create(event_id=event_id, user_id=user1.id)
            new_like.save()
            like_result = True
            like_message = 'like_success'

        return JsonResponse ({
            "like_num": like_event.current_rsvp,
            "like_result": like_result,
            "like_message": like_message
        }, safe=False)

class CommentView(View):

    def post(self, request, event_id):
        comment_data = json.loads(request.body)
        user1 = User.objects.get(id=comment_data["user_pk"])

        #새로운 댓글 로우데이터 작성
        new_comment = EventComment.objects.create(
            event_id=event_id, user_id=user1.id,
            comment_text=comment_data["comment_text"],
            created_at=comment_data["created_at"])
        new_comment.save()
        comment_result = True
        result_message = "comment_success"

        return JsonResponse ({
            "user_pk": user1.id,
            "user_name": user1.name,
            "message": result_message,
            "comment_result": True
        }, safe=False)

class NewEventView(View):

    def post(self, request):

        new_event = json.loads(request.body)
        user1 = User.objects.get(id=new_event['user_pk'])
        event_building = Building.objects.get(id=new_event['building_id'])

        new_event_data = EventPost.objects.create(title=new_event["title"], building=event_building, place=new_event["place"],date=new_event["date"], start_time=new_event["start_time"], end_time=new_event["end_time"],max_rsvp=new_event["max_rsvp"],main_text=new_event["main_text"],event_host=user1, photo_url=new_event["photo_url"]) 
        #추후 추가 필요  event_page_url=new_event["event_page_url"]
        new_event_data.save()
        message="event_register_success"

        EventPost.objects.filter
        return JsonResponse({
            "result_message": message,
            "event_id": new_event_data.id
        })