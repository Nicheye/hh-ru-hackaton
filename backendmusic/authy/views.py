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
from datetime import timedelta
from django.utils import timezone
from .filters import ProfileFilter
from django.core.mail import send_mail
from .models import EventReact
from .models import Redirection
def check(request):
     user = request.user
     if user.is_authenticated:
          if user.profile.email =="":
               user.profile.email =user.email
               user.save()
          
          from datetime import datetime
          from dateutil import relativedelta
          d = relativedelta.relativedelta(datetime.now(),user.profile.bday)
          user.profile.age = d.years
          user.profile.save()

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
     # permission_classes = [permissions.IsAuthenticated]
     
     def get(self,request,*args, **kwargs):
          if request.user.profile.is_proved ==True:
               pk = kwargs.get("pk", None)
               if not pk:
                    users = User.objects.all()
                    serializer = UserSerializer(users,many=True).data
                    check(request)
                    
                         
                    
                    return Response({"users":serializer})
                    
               else:
                    user = User.objects.get(id=pk)
                    profik = Profile.objects.get(user=user)
                    serializer = UserSerializer(user).data
                    return Response({"user": serializer})
          else:
               return Response({"message":"you ve not enough rights for this"})
     
     def put(self, request, *args, **kwargs):
        check(request)
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
        


class EventApi(APIView):
     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
     def get(self,request,*args,**kwargs):
          check(request)
          pk = kwargs.get("pk", None)
          utm = kwargs.get("utm", None)

          if utm:
               
               utm = str(utm).strip()
               print(utm)
               r = Redirection.objects.first()
               if utm =="vk":
                    r.vkcounter+=1
                    r.save()
               if utm =="habr":
                    r.habrcounter+=1
                    r.save()
               if utm =="tg":
                    r.tgcounter+=1
                    r.save()
               if utm =="yt":
                    r.ytcounter+=1
                    r.save()
               if (utm != "vk") and (utm != "tg") and (utm != "yt") and (utm != "habr"):
                    r.foreign+=1
                   
                    r.save()

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
                         myevents = InEvent.objects.filter(participant=request.user)
                         
                         from random import randint
                         for myevent in myevents:
                              if myevent.event.is_finished is True:
                                   myevent.place = randint(1,int(myevent.event.count))
                                   myevent.save()
                    
                    except:
                         pass
               serializer = EventSerializer(events,many=True).data
               return Response({"events":serializer})


     def post(self,request):
          check(request)
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
        check(request)
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

class EmailSender(APIView,AdminPermissionMixin):
     permission_classes = [IsAuthenticated]
     def get(self,request):
          check(request)
          pass
     
     def post(self,request,*args,**kwargs):
          check(request)
          pk = kwargs.get("pk", None)
          if pk:
               if pk=="all":
                    profiles = Profile.objects.all()
                    message = request.data['message']
                    
                    title = request.data['title']
                    for profile in profiles:
                         send_mail(
                         title,
                         message,
                         'settings.EMAIL_HOST_USER',
                         [profile.email],
                         fail_silently=False
                    )
                    return Response({"message":request.data})
               else:

                    profiles = Profile.objects.filter(role=pk)
                    message = request.data['message']
                    
                    title = request.data['title']
                    for profile in profiles:
                         send_mail(
                         title,
                         message,
                         'settings.EMAIL_HOST_USER',
                         [profile.email],
                         fail_silently=False
                    )
                    return Response({"message":request.data})
          else:

               message = request.data['message']
               email = request.data['email']
               title = request.data['title']
               send_mail(
                    title,
                    message,
                    'settings.EMAIL_HOST_USER',
                    [email],
                    fail_silently=False
               )
               return Response({"message":request.data})


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
class FilterApi(generics.ListAPIView):
     
     filter_backends=(DjangoFilterBackend,)
     serializer_class = ProfileSerializer
     filterset_class=ProfileFilter
     def get_queryset(self):
          queryset = Profile.objects.all()

class BigDataApi(APIView):
     def get(self,request):
          from datetime import datetime, timedelta
          thirty_days_ago = datetime.now() - timedelta(days=30)
          new_users_30 =User.objects.filter(date_joined__gte = thirty_days_ago)
          
          BACKEND=0
          UI =0
          Product_manager=0
          Front=0
          Fullstack=0
          Analyst=0
          Junior=0
          Middle=0
          Senior=0
          for new_user in new_users_30:
               if new_user.profile.role == 'BACKEND':
                    BACKEND+=1
               if new_user.profile.role == 'UI':
                    UI+=1
               if new_user.profile.role == 'Product_manager':
                    Product_manager+=1
               if new_user.profile.role == 'Front':
                    Front+=1
               if new_user.profile.role == 'Fullstack':
                    Fullstack+=1
               if new_user.profile.role == 'Analyst':
                    Analyst+=1
               if new_user.profile.grade =='Junior':
                    Junior+=1
               if new_user.profile.grade =='Middle':
                    Middle+=1
               if new_user.profile.grade =='Senior':
                    Senior+=1
          grades = {
               "Junior":Junior,
               "Middle":Middle,
               "Senior":Senior,
          }
          roles = {
               "BACKEND":BACKEND,
               "UI":UI,
               "Product_manager":Product_manager,
               "Front":Front,
               "Fullstack":Fullstack,
               "Analyst":Analyst,
          }
          from random import randint

          avg_time = randint(30,72)
          new_events =Event1.objects.filter(date_start__gte = thirty_days_ago)
          new_reacts = EventReact.objects.filter(date__gte = thirty_days_ago)
          return Response({
               "new_users_30":new_users_30.count(),
               "grades":grades,
               "roles":roles,
               "avg_time":avg_time,
               "new_events":new_events.count(),
               "new_reacts":new_reacts.count()
                           })
          
     
     