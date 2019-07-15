from user.models import User, UserType
from event.models.event_models import EventPost, EventRsvp, EventLike, EventComment
from event.models.building_models import Building
from django.views import View
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.utils.dateformat import DateFormat
from urllib import parse
import json

POST_DEFAULT_NUM = 8

def mypage_test(request):
    return HttpResponse("<h1>테스트</h1>")
class UserInfoView(View):

    def post(self, request):
        page_user    = json.loads(request.body)
        user_info    = list(User.objects.filter(id = page_user["user_pk"]).values())

        return JsonResponse(user_info, safe = False)

class MyRsvpListView(View):

    def post(self, request):
        page_user    = json.loads(request.body)
        user_info    = User.objects.get(id = page_user["user_pk"])
        my_rsvp_list = list(EventRsvp.objects.order_by('created_at').filter(
            user_id  = user_info.id
            ).select_related('user','event','building').values(
                'user__name',
                'event__title',
                'event__title',
                'event__photo_url',
                'event__date',
                'event__max_rsvp',
                'event__current_rsvp',
                'event__building__name',
                'created_at'
                ).all()[:POST_DEFAULT_NUM])

        return JsonResponse(my_rsvp_list, safe = False)

class MyLikeListView(View):

    def post(self, request):
        page_user    = json.loads(request.body)
        user_info    = User.objects.get(id = page_user["user_pk"])
        my_like_list = list(EventLike.objects.order_by('created_at').filter(
            user_id  = user_info.id
            ).select_related('user','event','building').values(
                'user__name',
                'event__title',
                'event__title',
                'event__photo_url',
                'event__date',
                'event__max_rsvp',
                'event__current_rsvp',
                'event__building__name',
                'created_at'
                ).all()[:POST_DEFAULT_NUM])

        return JsonResponse(my_like_list, safe = False)
