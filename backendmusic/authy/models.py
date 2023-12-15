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
		(FEMELE,'FEMLE'),
	]
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to="avatars")
	bio = models.CharField(max_length=1000,blank=True)
	role = models.CharField(max_length=16,choices=ROLE_CHOICES,default=Analyst)
	sex = models.CharField(max_length=16,choices=SEX_CHOICES,default=FEMELE)
	name = models.CharField(max_length=100,blank=True)
	second = models.CharField(max_length=100,blank=True)
	father = models.CharField(max_length=100,blank=True)
	phone = PhoneNumberField(null=False, blank=False,default="")
	bday=models.DateField(auto_now=False, auto_now_add=False,blank=True,default="2000-01-05")
	proved = models.BooleanField(default=False)
	admin = models.BooleanField(default=False)

	def create_user_profile(sender,instance,created,**kwargs):
		if created:
			Profile.objects.create(user=instance)
	def save_user_profile(sender,instance,**kwargs):
		instance.profile.save()
	
	post_save.connect(create_user_profile,sender=User)
	post_save.connect(save_user_profile,sender=User)
	