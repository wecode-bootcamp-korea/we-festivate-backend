
API 기능 정의서
================================



 event app
--------------------------------
1. 참가 신청

1) url:  ~/event/detail/1/rsvp


2) 요청라인

```
post
{"user_pk": 2}
```

3) 응답라인

성공 시
```
{
    "current_rsvp": 22,
    "rsvp_result": true,
    "rsvp_message": "rsvp_success"
}
```

이미 참가 신청 한 사람이 클릭 시 취소됨
```
{
    "current_rsvp": 22,
    "rsvp_result": true,
    "rsvp_message": "rsvp_success"
}
```

참가 제한 수 초과 시
```
{
    "current_rsvp": 3,
    "rsvp_result": false,
    "rsvp_message": "rsvp_overflow"
}
```



2. 참가 신청
1) url:  ~/event/detail/1/like


2) 요청라인

```
post
{"user_pk": 2}
```

3) 응답라인

성공 시
```
{
    "like_num": 3,
    "like_result": true,
    "like_message": "like_success"
}
```

이미 참가 신청 한 사람이 클릭 시 취소됨
```
{
    "like_num": 3,
    "like_result": false,
    "like_message": "like_canceled"
}
```



 mypage app
--------------------------------
1. my page 내 정보 가저오기

1) url: ~/mypage/user_info

2) 요청라인

```
post
{"user_pk": 2}
```

3) 응답라인

```
[
    {
        "id": 2,
        "user_id": "none",
        "password": "1234",
        "name": "none",
        "email": "none@none",
        "profile": "1234",
        "user_type_id": 1,
        "social_id_id": 1,
        "social_login_id": "none",
        "created_at": "2019-07-13T00:00:00Z",
        "updated_at": "2019-07-13T00:00:00Z"
    }
]

```

2. my page 참가 신청 리스트 구현
	
1) url: ~/mypage/rsvp

2) 요청 라인
	
```
post
{“user_pk”: 1}
		
```



3) 응답 라인		


```
[
    {
        "user__name": "testing",
        "event__title": "wecode, 당신을 코딩의 세계로 인도 합니다.",
        "event__photo_url": "https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/landing/bootcamp/boot_2.jpg",
        "event__date": "2019. 7. 13",
        "event__max_rsvp": 3,
        "event__current_rsvp": 3,
        "event__building__name": "Seolleung II",
        "created_at": "2019-07-13T12:14:59.439Z"
    },
    {
        "user__name": "testing",
        "event__title": "뉴멤버 오리엔테이션",
        "event__photo_url": "https://res-5.cloudinary.com/wework/image/upload/c_fill,h_460,w_460/v1561948688/production/event/photo/7ae6b39d-72f8-4aa4-b8b6-11a5f17f40bb.jpg",
        "event__date": "190701",
        "event__max_rsvp": 150,
        "event__current_rsvp": 22,
        "event__building__name": "Hongdae",
        "created_at": "2019-07-13T12:15:31.664Z"
    }
]
```



3. my page 좋아요 리스트 구현 

1) url: ~/mypage/like
2) 요청라인 / 응답라인은 모두 참가 리스트 구현과 동일