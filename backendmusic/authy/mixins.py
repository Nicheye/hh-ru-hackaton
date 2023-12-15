from rest_framework import permissions

class AdminPermissionMixin():
	permission_classes= [permissions.AllowAny]
	def has_permission(self,request,view):
		user = request.user
		if user.profile.admin == True:
			perms_map = {
			'GET': ['%(app_label)s.view_%(model_name)s'],
			'OPTIONS': [],
			'HEAD': [],
			'POST': ['%(app_label)s.add_%(model_name)s'],
			'PUT': ['%(app_label)s.change_%(model_name)s'],
			'PATCH': ['%(app_label)s.change_%(model_name)s'],
			'DELETE': ['%(app_label)s.delete_%(model_name)s'],
		}
class TakePartMixin():
	
	def has_permission(self,request):
		user = request.user
		if user.profile.proved ==True:
			pass
		else:
			return False