from django.db import models
from django.utils import timezone
from user.models  import User
from event.models.building_models import Building
class EventPost(models.Model):
    title = models.CharField(max_length=50)
    building = models.ForeignKey(Building, blank=True, null=True, on_delete=models.CASCADE, default=1)
    place = models.CharField(max_length=50)                     # 이벤트 진행 상세 위치  예) 8층 메인라운지
    date = models.CharField(max_length=10, blank=True)          # 이벤트 진행날짜
    stat_time = models.CharField(max_length=10, blank=True)     # 이벤트 시작시간
    end_time = models.CharField(max_length=10, blank=True)      # 이벤트 종료시간
    max_rsvp = models.IntegerField(blank=True)                  # 최대 신청 허용 인원
    current_rsvp = models.IntegerField(default=0)               # 현재 신청 인원
    event_page_url = models.URLField(max_length=100)            # members.wework.com 에 올려져있는 이벤트 url 링크
    main_text = models.TextField(max_length=2000 ,blank=True)   # 본문 내용
    photo_url = models.CharField(max_length=100, blank=True)    # 사진을 저장한 url
    event_host = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, default=1)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "event"
#app_label = "event"  (현재 버전에서는 필요 없다고 함)
