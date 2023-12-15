from rest_framework.views import APIView
from .serializers import UserSerializer,ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import User,Profile
from rest_framework import permissions
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
     
class UsersView(APIView):
     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
     def get(self,request,*args, **kwargs):
          pk = kwargs.get("pk", None)
          if not pk:
               users = User.objects.all()
               serializer = UserSerializer(users,many=True).data
               return Response({"users":serializer})
          else:
               user = User.objects.get(id=pk)
               profik = Profile.objects.get(user=user)
               serializer = ProfileSerializer(profik).data
               return Response({"user": serializer})
          
     def put(self, request, *args, **kwargs):
        
        pk = kwargs.get("pk", None)
        if request.user.id==pk:
          if not pk:
               return Response({"error": "Method PUT not allowed"})
     
          try:
               
               instance = Profile.objects.get(user=User.objects.get(pk=pk))
          except:
               return Response({"error": "Object does not exists"})
          if request.data['bio']:
               bio =request.data['bio'] 
          
          serializer = ProfileSerializer(data=request.data, instance=instance)
          serializer.is_valid(raise_exception=True)
          serializer.save()
     
          return Response({"user": serializer.data})
        else:
             return Response({"message": "it aint your profile u cant change it"})
        