from rest_framework import views,viewsets,status, generics,response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import CustomUserSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: views.Request, *args, **kwargs) -> views.Response:
        print("in login response", request.user, args, kwargs,request.data)
        try:
            res =  super().post(request, *args, **kwargs)
            print(res,'response',request.user)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            res.data['user_id'] = user.id
            res.data['user'] = user.username
            print(user,'user')
            return res
        except Exception as e:
            print(e, 'exeption')
            return response.Response(data=str(e),status=status.HTTP_404_NOT_FOUND)