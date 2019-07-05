import jwt
import json
import bcrypt

from .models import User
from django.views import View
from django.http import JsonResponse, HttpResponse



class UserView(View):
    def get(self, request):
        return HttpResponse("문자열 하나 써보죠")
    
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

# class LoginView(View):
#     def post(self, request):
#         login_user_info = json.loads(request, body)
#         encoded_jwt = jwt.encode({'user_id': },, algorithm='HS256')        
#         user = User.objects.get(id = user_id)

#         if bcrypt.checkpw(login_user_info['password'].encode('UTP-8'), user.password.encode("UTF-8"):
#             return jsonResponse(
#                 {
                    
#             )
        
          
                    

        
