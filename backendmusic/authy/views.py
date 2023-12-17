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
     users = User.objects.all()
     for user in users:
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
     permission_classes = [permissions.IsAuthenticated]
     
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
                    from .serializers import UserDataSeriailizer
                    serializer = UserDataSeriailizer(profik).data
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
               events =Event1.objects.filter(is_finished=False).order_by('-id').all()
               

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
          
     
class EventData(APIView):
     def get(self,request,*args,**kwargs):
          pk = kwargs.get("pk", None)
          event= Event1.objects.get(id=pk)
          from .serializers import EventDataSerializer
          event_ser =EventDataSerializer(event).data
          return Response({"event":event_ser})

class AnalyticsData(APIView):
     def get(self,request,*argsm,**kwargs):
          check(request)
          from random import randint
          avg_time = randint(50,120)
          all_time = avg_time*(randint(5,10))
          last_24hours = randint(30,70)
          five_days_ago = datetime.datetime.now() - timedelta(days=30)
          new_reacts = EventReact.objects.filter(date__gte = five_days_ago)
          all=0
          good=0
          bad=0
          for react in new_reacts:
               all+=1
               if react.react =='Good':
                    good+=1
               if react.react =='Bad':
                    bad+=1     
          loyalty = good/all*100
          all_events = Event1.objects.all()
          sum =0
          budget=0
          BACKEND=0
          UI =0
          Product_manager=0
          Front=0
          Fullstack=0
          Analyst=0
          all_events_count=all_events.count()
          from .models import EventTag
          for event in all_events:
               sum+=event.merch+event.rent+event.keytering
               budget+=event.event_money
               tags = EventTag.objects.filter(event=event)
               if tags.count()>0:
                    for tag in tags:
                         if tag=='BACKEND':
                              BACKEND+=1
                         if tag=='UI':
                              UI+=1    
                         if tag=='Product_manager':
                              Product_manager+=1   
                         if tag=='Front':
                              Front+=1   
                         if tag=='Fullstack':
                              Fullstack+=1     
                         if tag=='Analyst':
                              Analyst+=1 
          doneningevents = sum/budget *100 
          tags = {
               "BACKEND":str(round(BACKEND/all_events_count *100))+"%",
               "UI":str(round(UI/all_events_count*100)) +"%" ,
               "Product_manager":str(round(Product_manager/all_events_count *100)) +"%",
               "Front":str(round(Front/all_events_count *100))+"%",
               "Fullstack":str(round(Fullstack/all_events_count *100))+"%",
               "Analyst":str(round(Analyst/all_events_count *100))+"%",
          }
          all_users = Profile.objects.all()
          count_users =all_users.count()
          males=0
          females=0
          
          four_seven=0
          eight_twenty=0
          twenty_twhirsty=0
          twhirsty_fourty=0
          ff_54=0
          more=0

          Moskva=0
          Piter=0
          Novosib=0
          Ekb=0
          Kazan=0
          Others=0

          Jun=0
          Mid=0
          Sen=0


          back=0
          ui=0
          pm=0
          fr=0
          fs=0
          anal=0

          beginner=0
          expirienced=0
          fan=0

          for profile in all_users:
               if profile.status=='beginner':
                    beginner+=1
               if profile.status=='expirienced':
                    expirienced+=1
               if profile.status=='fan':
                    fan+=1
               if profile.role =='BACKEND':
                    back+=1

               if profile.role =='UI':
                    ui+=1

               if profile.role =='Product manager':
                    pm+=1

               if profile.role =='Frontend':
                    fr+=1
               if profile.role =='Fullstack':
                    fs+=1
               if profile.role =='Analyst':
                    anal+=1


               if profile.sex =='MALE':
                    males+=1
               else:
                    females+=1
               if profile.age>=14 and profile.age<=17:
                    four_seven+=1
               if profile.age>=18 and profile.age<=24:
                    eight_twenty+=1
               if profile.age>=25 and profile.age<=34:
                    twenty_twhirsty+=1
               if profile.age>=35 and profile.age<=44:
                    twhirsty_fourty+=1
               if profile.age>=45 and profile.age<=54:
                    ff_54+=1
               if profile.age>54:
                    more+=1
               if profile.city =='Moskva':
                    Moskva+=1
               if profile.city =='spb':
                    Piter+=1  
               if profile.city =='Novosib':
                    Novosib+=1
               if profile.city =='Ekb':
                    Ekb+=1
               if profile.city =='Kazan':
                    Kazan+=1
               if profile.city !='spb' and profile.city !='Moskva' and profile.city !='Novosib' and profile.city !='Ekb' and profile.city !='Kazan':

                    Others+=1
               if profile.grade =='Junior':
                    Jun+=1
               if profile.grade =='Middle':
                    Mid+=1
               if profile.grade =='Senior':
                    Sen+=1



          age_tags={
               '14_17':str(round(four_seven/count_users*100))+"%",
               '18_24':str(round(eight_twenty/count_users*100))+"%",
               '25_34':str(round(twenty_twhirsty/count_users*100))+"%",
               '35_44':str(round(twhirsty_fourty/count_users*100))+"%",
               '45_54':str(round(ff_54/count_users*100))+"%",
               'more':str(round(more/count_users*100))+"%",
          }

          role_tags={
               "backends":str(round(back/count_users*100))+"%",
               "ui":str(round(ui/count_users*100))+"%",
               "Product manager":str(round(pm/count_users*100))+"%",
               "frontends":str(round(fr/count_users*100))+"%",
               "fullstacks":str(round(fs/count_users*100))+"%",
               "analysts":str(round(anal/count_users*100))+"%",

          }
          status_tags={
               "begginer_users":str(round(beginner/count_users*100))+"%",
               "expirienced_users":str(round(expirienced/count_users*100))+"%",
               "fan":str(round(fan/count_users*100))+"%",
          }
          sex_tags = {
               'Males':str(round(males/count_users*100))+"%",
               'females':str(round(females/count_users*100))+"%",
          }
          
          city_tags={
               'Moscow':str(round(Moskva/count_users*100))+"%",
               'Saint-P':str(round(Piter/count_users*100))+"%",
               'Novosib':str(round(Novosib/count_users*100))+"%",
               'Ekb':str(round(Ekb/count_users*100))+"%",
               'Kazan':str(round(Kazan/count_users*100))+"%",
               'others':str(round(Others/count_users*100))+"%",
          }

          grade_tags = {
               'Juniors':str(round(Jun/count_users*100))+"%",
               'Middle':str(round(Mid/count_users*100))+"%",
               'Senior':str(round(Sen/count_users*100))+"%",
          }
          socials={
               "vk":str(randint(10,30))+"%",
               "tg":str(randint(20,40))+"%",
               "others":str(randint(15,30))+"%",
          }


          sended_sms = randint(100,700)
          responded_sms = randint(100,300)
          conversion_sms=str(randint(10,60))+"%"
          sended_email = randint(600,1400)
          responded_email = randint(250,404)
          conversion_email=str(randint(17,70))+"%"
          sended_msg = randint(350,600)
          responded_msg = randint(20,300)
          conversion_msg=str(randint(5,60))+"%"
          return Response({
               "avg_time":avg_time,
               "all_time":all_time,
               "last_24hours":last_24hours,
               'loyalty':str(round(loyalty))+"%",
               'all_events':all_events_count,
               "all_spends":sum,
               "budget":budget,
               'doneningevents':str(round(doneningevents))+"%",
               "event_tags":tags,
               "count_users":count_users,
               "sex_tags":sex_tags,
               "age_tags":age_tags,
               "city_tags":city_tags,
               "grade_tags":grade_tags,
               "role_tags":role_tags,
               "socials":socials,
               "sended_sms":sended_sms,
               "responded_sms":responded_sms,
               "conversion_sms":conversion_sms,
               "sended_email":sended_email,
               "responded_email":responded_email,
               "conversion_email":conversion_email,
               "sended_msg":sended_msg,
               "responded_msg":responded_msg,
               "conversion_msg":conversion_msg,
               "statuses":status_tags
          })


