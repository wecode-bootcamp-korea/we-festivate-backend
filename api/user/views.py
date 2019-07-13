import jwt
import json
import bcrypt
import requests

from .models import User, SocialPlatform
from django.views import View
from django.http import JsonResponse
from api.settings import wef_key

class UserView(View):
    def post(self, request):
        new_user_info = json.loads(request.body)

        if User.objects.filter(email=new_user_info['email']).exists():
            return JsonResponse({'message' : '이미 가입된 이메일 주소입니다.'}, status=400)

        if User.objects.filter(user_id=new_user_info['user_id']).exists():
            return JsonResponse({'message' : '이미존재하는 아이디입니다.'}, status=400)
        
        password = bytes(new_user_info["password"], "utf-8")
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        new_user_info = User(
                user_id  = new_user_info['user_id'],
                password = hashed_password.decode("UTF-8"),
                name     = new_user_info['name'],
                email    = new_user_info['email'],
                profile  = new_user_info['profile'],
                #user_type = int(new_user_info['user_type']),
                #member_building = new_user_info['member_building'],
                )
        new_user_info.save()

        return JsonResponse({'message' : '회원가입이 완료되었습니다.'}, status = 200)

class LoginView(View):

    def post(self, request):
        '''
        로그인 순서
        유저가 아이디, 패스워드 입력 > 받은 데이터 변수에 저장하기 => 완료
        암호화한 패스워드랑 유저가 입력한 패스워드랑 비교
        로그인성공하면 access token을 클라이언트에게 전송
        다음부터는 access token을 첨부해서 request를 서버에 전송함으로써 매번 로그인해도 되지 않도록 한다.
        '''
        login_user_info = json.loads(request.body) #받은 데이터 변수에 저장
        login_user_id = login_user_info['user_id'] #아이디만 따로 변수에 저장

        if not User.objects.filter(user_id = login_user_id).exists(): # 디비에 입력된 아이디가 있는지 확인하고, 없으면 아래 메세지 리턴
            return JsonResponse ({'message':'가입된 아이디가 아닙니다.'}, status = 400)

        user = User.objects.get(user_id = login_user_id) #위에서 통과되면 유저아이디와 같은 값을 DB에서 찾아서 변수에 저장   
        
        if bcrypt.checkpw(login_user_info['password'].encode('UTF-8'), user.password.encode("UTF-8")): #패스워드가 일치하는지 확인
            encoded_jwt = jwt.encode({'id':user.id}, wef_key, algorithm='HS256') # jwt토큰 생성

            return JsonResponse({
                'access_token' : encoded_jwt.decode('UTF-8'),
                'user_name'    : user.name,
                #'user_type_id' : user.user_type.id,
                'user_pk'        : user.id
            }, status = 200)
        else:
            return JsonResponse({'message': '패스워드가 일치하지 않습니다.'}, status = 400)

class GoogleLoginView(View):
    # 소셜로그인을 하면 User테이블에 아이디와 패스워드를 담아두고
    # 카카오는 아이디 기준, 구글은 sub 기준으로 social_login_id에 저장
    # 이메일 같은게 있다면 토큰생성 및 전달 = 200 ok
    # 소셜 회원가입 유저의 타입(권한)은 nonmember로만 할 것인지? 혹은,, 로그인 후 추가 페이지를 생성해서 위워크의 내용이 있는지 검토? > 
    
    def get(self,request): # id_token만 해서 헤더로 받기
        token = request.headers["Authorization"] # 프론트엔드에서 HTTP로 들어온 헤더에서 id_token(Authorization)을 변수에 저장
        url = 'https://oauth2.googleapis.com/tokeninfo?id_token=' # 토큰을 확인하기 위한 gogle api
        response = requests.get(url+token) #구글에 id_token을 보내 디코딩 요청
        user = response.json() # 바이트화로 받은 유저정보를 디코딩된 유저의 정보를 json화해서 변수에 저장

        if User.objects.filter(social_login_id=user['sub']).exists(): #기존에 소셜로그인을 했었는지 확인
            user_info = User.objects.get(social_login_id=user['sub'])
            encoded_jwt = jwt.encode({'id': user["sub"]}, wef_key, algorithm='HS256') # jwt토큰 발행
            none_member_type = 1

            return JsonResponse({
                'access_token': encoded_jwt.decode('UTF-8'),
                'user_name'   : user['name'],
                'user_type'   : none_member_type,
                'user_pk'     : user_info.id
            }, status = 200)            
        else:          # 현재 이메일이 고유값인데 이메일이 없을 경우 따로 저장할 수 있는 if문을 추가해야 할 지?
            new_user_info = User(
                social_login_id = user['sub'],
                name            = user['name'],
                social          = SocialPlatform.objects.get(platform ="google"),
                email           = user.get('email', None)
            )
            new_user_info.save()
            encoded_jwt = jwt.encode({'id': new_user_info.id}, wef_key, algorithm='HS256') # jwt토큰 발행
            none_member_type = 1
        
            return JsonResponse({
            'access_token': encoded_jwt.decode('UTF-8'),
            'user_name'   : new_user_info.name,
            'user_type'   : none_member_type,
            'user_pk'     : new_user_info.id,
            }, status = 200)
            
class KakaoLoginView(View): #카카오 로그인

    def get(self, request):
        access_token = request.headers["Authorization"]
        headers =({'Authorization' : f"Bearer {access_token}"})
        url = "https://kapi.kakao.com/v1/user/me"
        response = requests.request("POST", url, headers=headers)
        user = response.json()

        if User.objects.filter(social_login_id=user['id']).exists(): #기존에 소셜로그인을 했었는지 확인
            user_info = User.objects.get(social_login_id=user['id'])
            encoded_jwt = jwt.encode({'id': user_info.id}, wef_key, algorithm='HS256') # jwt토큰 발행
            none_member_type = 1

            return JsonResponse({ #jwt토큰, 이름, 타입 프론트엔드에 전달
                'access_token': encoded_jwt.decode('UTF-8'),
                'user_name'   : user_info.name,
                'user_type'   : none_member_type,
                'user_pk'     : user_info.id
            }, status = 200)            
        else:
            new_user_info = User(
                social_login_id = user['id'],
                name            = user['properties']['nickname'],
                social          = SocialPlatform.objects.get(platform ="kakao"),
                email           = user['properties'].get('email', None)
            )
            new_user_info.save()
            encoded_jwt = jwt.encode({'id': new_user_info.id}, wef_key, algorithm='HS256') # jwt토큰 발행
            none_member_type = 1
            return JsonResponse({
                'access_token': encoded_jwt.decode('UTF-8'),
                'user_name'   : new_user_info.name,
                'user_type'   : none_member_type,
                'user_pk'     : new_user_info.id,
                }, status = 200)