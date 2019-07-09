import jwt
import json
import bcrypt

from .models import User
from django.views import View
from django.http import JsonResponse, HttpResponse
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
                user_id = new_user_info['user_id'],
                password = hashed_password.decode("UTF-8"),
                name = new_user_info['name'],
                email = new_user_info['email'],
                profile = new_user_info['profile'],
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
            encoded_jwt = jwt.encode({'user.id':user.id}, wef_key, algorithm='HS256') # jwt토큰 생성
            return JsonResponse({
                'access_token': encoded_jwt.decode("UTF-8"),
                'user_name': user.name,
                'user_type_id': user.user_type_id
            }, status = 200)
        else:
            return JsonResponse({'message': '패스워드가 일치하지 않습니다.'}, status = 400)
