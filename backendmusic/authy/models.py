from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField
class User(AbstractUser):
	username = models.CharField(max_length=255,unique=True)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []
	def profile(self):
		profile = Profile.objects.get(user=self)
	

class Profile(models.Model):
	BACKEND ='BACKEND'
	UI ='UI/UX'
	Product_manager ='Product manager'
	Project_manager ='Project manager'
	Front ='Frontend'
	Fullstack ='Fullstack'
	Analyst = 'Analyst'
	ROLE_CHOICES = [
		(BACKEND,'BACKEND'),
		(UI,'UI'),
		(Product_manager,'Product manager'),
		(Project_manager,'Project manager'),
		(Front,'Frontend'),
		(Fullstack,'Fullstack'),
		(Analyst,'Analyst'),
	]
	MALE = 'MALE'
	FEMELE='FEMALE'
	SEX_CHOICES = [
		(MALE,'MALE'),
		(FEMELE,'FEMELE'),
	]
	Junior = 'Junior'
	Middle='Middle'
	Senior='Senior'
	GRAD_CHOICES = [
		(Junior,'Junior'),
		(Middle,'Middle'),
		(Senior,'Senior'),
	]
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to="media/avatars",default="../media/avatars/123.png",blank=True)
	bio = models.CharField(max_length=1000,blank=True)
	role = models.CharField(max_length=16,choices=ROLE_CHOICES,default=Analyst)
	sex = models.CharField(max_length=16,choices=SEX_CHOICES,default=FEMELE)
	name = models.CharField(max_length=100,blank=True)
	second = models.CharField(max_length=100,blank=True)
	father = models.CharField(max_length=100,blank=True)
	phone = PhoneNumberField(null=False, blank=False,default="")
	bday=models.DateField(auto_now=False, auto_now_add=False,blank=True,default="2000-01-05")
	is_proved = models.BooleanField(default=False)
	
	admin = models.BooleanField(default=False)
	grade = models.CharField(max_length=10,choices=GRAD_CHOICES,default=Junior)
	city = models.CharField(max_length=50,default="Moskva")
	tg = models.CharField(max_length=32,default="@bot")
	email = models.EmailField(max_length = 254,default="")
	#сде
	def __str__(self) -> str:
		return str(self.user)+"|"+str(self.id)
	def create_user_profile(sender,instance,created,**kwargs):
		if created:
			Profile.objects.create(user=instance)
	def save_user_profile(sender,instance,**kwargs):
		instance.profile.save()
	
	post_save.connect(create_user_profile,sender=User)
	post_save.connect(save_user_profile,sender=User)
	events_count = models.PositiveIntegerField(default=0)
	prizes_count = models.PositiveIntegerField(default=0)
class Event(models.Model):
	BACKEND ='BACKEND'
	UI ='UI/UX'
	Product_manager ='Product manager'
	Project_manager ='Project manager'
	Front ='Frontend'
	Fullstack ='Fullstack'
	Analyst = 'Analyst'
	TAGS_CHOICES = [
		(BACKEND,'BACKEND'),
		(UI,'UI'),
		(Product_manager,'Product '),
		(Project_manager,'Project '),
		(Front,'Frontend'),
		(Fullstack,'Fullstack'),
		(Analyst,'Analyst'),
	]
	Hackaton ='Hackaton'
	Meetup ='Meetup'
	
	EVENT_TYPE_CHOICES = [
		(Hackaton,'Hackaton'),
		(Meetup,'Meetup'),
		
	]
	
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=700)
	image = models.ImageField(upload_to="media/avatars",default="../media/avatars/123.png",blank=True)
	tags=  models.CharField(max_length=30,choices=TAGS_CHOICES,blank=True,default=Fullstack)
	date = models.DateField(auto_now=False, auto_now_add=False,default=None)
	count = models.PositiveIntegerField(default=0)
	is_finished = models.BooleanField(default=False)
	views_count = models.PositiveIntegerField(default=0)
	event_type = models.CharField(max_length=12,choices=EVENT_TYPE_CHOICES,default="123")
	def __str__(self) -> str:
		return str(self.title)
class InEvent(models.Model):
	place = models.PositiveIntegerField(default=0)
	participant = models.ForeignKey(User,on_delete=models.CASCADE)
	event = models.ForeignKey(Event,on_delete=models.CASCADE)
	def __str__(self) -> str:
		return str(self.participant) + " | "+str(self.event)