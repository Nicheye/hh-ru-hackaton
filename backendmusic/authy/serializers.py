from rest_framework import serializers
from .models import User,Profile,Event
from django.utils import timezone
from .models import InEvent
class UserSerializer(serializers.ModelSerializer):
	ava = serializers.SerializerMethodField()
	role = serializers.SerializerMethodField()
	sex = serializers.SerializerMethodField()
	name=serializers.SerializerMethodField()
	second=serializers.SerializerMethodField()
	father=serializers.SerializerMethodField()
	age = serializers.SerializerMethodField()
	city = serializers.SerializerMethodField()
	phone = serializers.SerializerMethodField()
	events_count = serializers.SerializerMethodField()
	grade = serializers.SerializerMethodField()
	tg = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields =['id','username','password','email','name','second','father','city','ava','role','sex','phone','age','events_count','grade','tg']
		extra_kwargs = {
			'password':{'write_only':True}
		}
	def get_ava(self,obj):
		return "http://127.0.0.1:8000"+obj.profile.avatar.url
	def get_role(self,obj):
		return obj.profile.role
	def get_grade(self,obj):
		return obj.profile.grade
	def get_phone(self,obj):
		return str(obj.profile.phone)
	def get_tg(self,obj):
		return obj.profile.tg
	def get_sex(self,obj):
		return obj.profile.sex
	def get_name(self,obj):
		return obj.profile.name
	def get_events_count(self,obj):
		return obj.profile.events_count
	def get_age(self,obj):
		from datetime import datetime
		from dateutil import relativedelta
		delte=relativedelta.relativedelta(datetime.now(),obj.profile.bday)
		return str(delte.years)
	def get_city(self,obj):
		return obj.profile.city
	def get_second(self,obj):
		return obj.profile.second

	def get_father(self,obj):
		return obj.profile.father

	def create(self,validated_data):
		password = validated_data.pop('password',None)
		instance =  self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance
	
class ProfileSerializer(serializers.ModelSerializer):
	age = serializers.SerializerMethodField()

	class Meta:
		model = Profile
		fields =('avatar','bio','role','sex','name','second','father','phone','bday','age','city')
	def get_age(self,obj):
		from datetime import datetime
		from dateutil import relativedelta
		delte=relativedelta.relativedelta(datetime.now(),obj.bday)
		return int(delte.years)
	def update(self, instance, validated_data):
			
			instance.avatar = validated_data.get("avatar", instance.avatar)
		
			instance.bio = validated_data.get("bio", instance.bio)
			instance.role = validated_data.get("role", instance.role)
			instance.sex = validated_data.get("sex", instance.sex)
			instance.name = validated_data.get("name", instance.name)
			instance.second = validated_data.get("second", instance.second)
			instance.father = validated_data.get("father", instance.father)
			instance.phone = validated_data.get("phone", instance.phone)
			instance.bday = validated_data.get("bday", instance.bday)

			instance.save()
			return instance
	
class UserDataSeriailizer(serializers.ModelSerializer):
	age = serializers.SerializerMethodField()
	wins = serializers.SerializerMethodField()
	winrate = serializers.SerializerMethodField()
	time = serializers.SerializerMethodField()
	teams = serializers.SerializerMethodField()
	class Meta:
		model = Profile
		fields =('avatar','bio','role','sex','name','second','father','phone','bday','age','city','events_count','wins','winrate','time','teams')
	def get_age(self,obj):
		from datetime import datetime
		from dateutil import relativedelta
		delte=relativedelta.relativedelta(datetime.now(),obj.bday)
		return int(delte.years)
	def get_wins(self,obj):

		wins = InEvent.objects.filter(participant=obj.user,place=1).count()
		obj.wins = wins
		obj.save()
		return wins
	def get_winrate(self,obj):
		return str(obj.wins/obj.events_count * 100) + "%"
	def get_time(self,obj):
		from random import randint
		return str(randint(150,700))+" min"
	def get_teams(self,obj):
		from .models import Team,TeamPart
		teams = TeamPart.objects.filter(user=obj.user)
		titles = []
		for team in teams:
			titles.append(team.team.title)
		return titles

from .models import EventTag
class EventSerializer(serializers.ModelSerializer):
	img = serializers.SerializerMethodField()
	tags= serializers.SerializerMethodField()
	class Meta:
		model = Event
		fields =('title','description','img','tags','date','count','views_count','tags')
	def get_img(self,obj):
		return "http://127.0.0.1:8000"+obj.image.url
	def get_tags(self,obj):
		a = EventTag.objects.filter(event=obj)
		tags=[]
		for opium in a:
			tags.append(opium.tags)
		return tags

class EventDataSerializer(serializers.ModelSerializer):
	img = serializers.SerializerMethodField()
	tags= serializers.SerializerMethodField()
	spents = serializers.SerializerMethodField()
	redirects =serializers.SerializerMethodField()
	registers = serializers.SerializerMethodField()
	class Meta:
		model = Event
		fields =('title','description','img','tags','date','registers','views_count','tags','event_money','spents','redirects')
	def get_img(self,obj):
		return "http://127.0.0.1:8000"+obj.image.url
	def get_registers(self,obj):
		return obj.count
	def get_spents(self,obj):
		return obj.rent+obj.merch+obj.keytering
	def get_redirects(self,obj):
		return round(obj.views_count*1.25)
	def get_tags(self,obj):
		a = EventTag.objects.filter(event=obj)
		tags=[]
		for opium in a:
			tags.append(opium.tags)
		return tags

	
	