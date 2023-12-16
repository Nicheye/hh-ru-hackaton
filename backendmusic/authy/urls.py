
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *
urlpatterns = [
      path('home/',HomeView.as_view(), name ='home'),
	path('logout/', LogoutView.as_view(), name ='logout'),
      path('register/',RegisterView.as_view()),
	path('users/',UsersView.as_view()),#список пользователей для админа
	path('users/<int:pk>/', UsersView.as_view()), #получение конкретного пользователя для админа
	path('events/', EventApi.as_view()),#список евентов для юзера
	path('events/<int:pk>/', EventApi.as_view()),#переход на конкретный ивент
	path('event/<int:pk>/register',EventRegister.as_view()),#рега на ивент конкретный
	path('emailsend/',EmailSender.as_view()),#для админа рассылка по имейоу
	path('emailsend/<slug:pk>/',EmailSender.as_view()),
	path('filtering',FilterApi.as_view())
	
]