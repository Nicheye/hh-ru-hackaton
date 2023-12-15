from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.mail import send_mail
class HomeView(APIView):
   permission_classes = (IsAuthenticated, )
   def get(self, request):
       user = UserSerializer(request.user).data
       return Response({"user":user})
   
class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
class RegisterView(APIView):
	def post(self,request):
               serializer =  UserSerializer(data=request.data)
               serializer.is_valid(raise_exception=True)
               serializer.save()
               email = serializer.data['email']
               send_mail(
                    'You have registered to gameboard',
                    'Welcome to gay party',
                    'settings.EMAIL_HOST_USER',
                    [email],fail_silently=False

               )
               return Response(serializer.data)
     
class ProfileView(APIView):
     def get(self,request):
          user = UserSerializer(request.user).data
          return Response({"user":user})