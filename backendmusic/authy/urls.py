
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *
urlpatterns = [
      path('home/',HomeView.as_view(), name ='home'),
	path('logout/', LogoutView.as_view(), name ='logout'),
      path('register/',RegisterView.as_view()),
	path('users/',UsersView.as_view()),
	path('users/<int:pk>/', UsersView.as_view()),
	path('events/', EventApi.as_view()),
	path('events/<int:pk>/', EventApi.as_view()),
	path('event/<int:pk>/register',EventRegister.as_view())
]