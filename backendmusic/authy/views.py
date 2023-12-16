from rest_framework.views import APIView
from .serializers import UserSerializer,ProfileSerializer,EventSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .mixins import AdminPermissionMixin
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import User,Profile,InEvent
from .models import Event as Event1
from django.shortcuts import get_object_or_404
from rest_framework import permissions
import datetime
from django.utils import timezone
from django.core.mail import send_mail
class HomeView(APIView):
   permission_classes = (IsAuthenticated, )
   def get(self, request):
       user = UserSerializer(request.user).data
       if request.user.profile.role is not None and (request.user.profile.sex is not None) and (request.user.profile.name is not None) and (request.user.profile.second is not None) and (request.user.profile.phone !=""):
          request.user.profile.is_proved = True
          request.user.profile.save()
          
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
               from rest_framework_simplejwt import views as jwt_views
               # jwt_views.TokenObtainPairView.perform_authentication({"username":serializer.data['username'],"password":serializer.data['password']})
               return Response(serializer.data)
     
class UsersView(APIView):
     permission_classes = [permissions.IsAuthenticated]
     
     def get(self,request,*args, **kwargs):
          if request.user.profile.is_proved ==True:
               pk = kwargs.get("pk", None)
               if not pk:
                    users = User.objects.all()
                    serializer = UserSerializer(users,many=True).data
                    for user in users:
                         if user.profile.email =="":
                              user.profile.email =user.email
                              user.save()
                    
                    return Response({"users":serializer})
                    
               else:
                    user = User.objects.get(id=pk)
                    profik = Profile.objects.get(user=user)
                    serializer = ProfileSerializer(profik).data
                    return Response({"user": serializer})
          else:
               return Response({"message":"you ve not enough rights for this"})
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
        
class EmailSender(APIView,AdminPermissionMixin):
     def get(self,request):
          pass
     def post(self,request):
          pass

class EventApi(APIView):
     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
     def get(self,request,*args,**kwargs):
          pk = kwargs.get("pk", None)
          if pk:
               event = get_object_or_404(Event1,id=pk)
               event.views_count+=1
               event.save()
               serializer = EventSerializer(event).data
               return Response({"events":serializer})

          else:
               events =Event1.objects.filter(is_finished=False).all()
               

               for event in events:
                    from datetime import datetime, date
                    import pytz
                    dt = datetime.now()
                    if event.date>datetime.date(dt):
                         pass
                    else:
                         event.is_finished=True
                         event.save()
               if request.user.is_authenticated:
                    try:
                         myevents = InEvent.objects.filter(user=request.user)
                         from random import randint
                         for myevent in myevents:
                              if myevent.event.is_finished ==True:
                                   myevent.place = randint(1,int(myevent.event.count))
                                   myevent.save()
                    
                    except:
                         pass
               serializer = EventSerializer(events,many=True).data
               return Response({"events":serializer})


     def post(self,request):
          if request.user.is_superuser or request.user.profile.admin ==True:
               serializer = EventSerializer(data=request.data)
               serializer.is_valid(raise_exception=True)
               serializer.save()
               return Response(serializer.data)
          else:
               return Response({"message":"u r not admin"})
class EventRegister(APIView):
     permission_classes = [permissions.IsAuthenticated]
     def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        
        if request.user.profile.is_proved ==True:
             event = Event1.objects.get(id=pk)
             
             try:
                  ain = InEvent.objects.get(participant=request.user,event=event)
                  return Response({"message":"you are in"})
             except:
               new_event = InEvent()
               event.count +=1
               new_event.participant = request.user
               new_event.event = event
               new_event.save()
               request.user.profile.events_count+=1
               request.user.profile.save()
               event.save()
               return Response({"message":"you have been registered"})
             
        else:
             return Response({"message":"u r not proved"})
