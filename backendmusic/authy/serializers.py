from rest_framework import serializers
from .models import User,Profile
class UserSerializer(serializers.ModelSerializer):
	ava = serializers.SerializerMethodField()
	bio = serializers.SerializerMethodField()
	role = serializers.SerializerMethodField()
	sex = serializers.SerializerMethodField()
	
	class Meta:
		model = User
		fields =['id','username','password','email','ava','bio','role','sex',]
		extra_kwargs = {
			'password':{'write_only':True}
		}
	def get_ava(self,obj):
		return "http://127.0.0.1:8000"+obj.profile.avatar.url
	def get_bio(self,obj):
		return obj.profile.bio
	def get_role(self,obj):
		return obj.profile.role
	def get_sex(self,obj):
		return obj.profile.sex
	
	def create(self,validated_data):
		password = validated_data.pop('password',None)
		instance =  self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance
	
class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields =('avatar','bio','role','sex','name','second','father','phone','bday')
		
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