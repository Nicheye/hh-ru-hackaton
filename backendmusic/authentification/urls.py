
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *
urlpatterns = [
      path('home/',HomeView.as_view(), name ='home'),
	path('logout/', LogoutView.as_view(), name ='logout'),
      path('register/',RegisterView.as_view()),
	path('profile',ProfileView.as_view())
]