from user.models import User
from api.settings import wef_key
from django.http import JsonResponse
import jwt
import json

def login_required(func):
    '''
    로그인 데코레이터_2차
    목적: 홈페이지 권한(로그인, 혹은 관리자)을 가진 유저만 이용가능한 서비스를 해당 유저가 맞는지 
    데코레이터를 통해 확인하고, 정상적으로 로그인한 유저인지 확인하기 위한 데코레이터를 구현
    1) 프론트엔드에 전달했던 access_token을 http 헤더로 전달받고,
    >>토큰이 없으면 JsonResponse ({"error_code"":"INVALID_LOGIN"}, status=400)
    2) jwt를 decode하고,
    >> 오류나면 JsonResponse({"error_code" : "INVALID_TOKEN"}, status = 401) 
    3) DB(models)에서 jwt로 decode된 payload의 아이디와 일치하는 user의 정보를 변수에 저장
    >> 오류나면 JsonResponse({"error_code" : "UNKNOWN_USER"}, status = 401)
    4) jwt토큰이 decode 됐다는 것은 해당 토큰을 서버에서 발행된 것이라는게 확인되기 때문에 request할 객체에 user변수를 수정한다.
    5) request에 유저정보를 포함해서 리턴해준다.
    6) 테스트 실행 후 오류가 있는지 확인 
    '''
    def wrapper(self, request, *args, **kwargs): #access token이 헤더에 들어있음
    
        if "Authorization" not in request.headers: #1)번
            return JsonResponse({"error_code":"INVALID_LOGIN"}, status=401)
        
        encode_token = request.headers["Authorization"] 

        try:
            data = jwt.decode(encode_token, wef_key, algorithm='HS256') #2번)decode를 하게 될 경우 프론트엔드에 전달했던 페이로드값만 나옴(즉 로그인뷰에 바디)
            
            user = User.objects.get(id = data["id"])#3번
            
            request.user = user #4번

        except jwt.DecodeError: #2번 error
            return JsonResponse({
                "error_code" : "INVALID_TOKEN"
            }, status = 401) # 401에러 : 권한이 없을때 발생
        
        except User.DoesNotExist:
            return JsonResponse({
                "error_code" : "UNKNOWN_USER"
            }, status = 401) # 401에러 : 권한이 없을때 발생

        return func(self, request, *args, **kwargs) #5번

    return wrapper





        


    
        
         
