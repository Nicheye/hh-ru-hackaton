from django_filters import rest_framework as filters
from datetime import datetime
from dateutil import relativedelta
from .models import Profile
class CharFilterInFilter(filters.BaseInFilter,filters.CharFilter):
	pass
class ProfileFilter(filters.FilterSet):
	#delte=relativedelta.relativedelta(datetime.now(),obj.profile.bday)
	age = filters.RangeFilter()
	sex = CharFilterInFilter(field_name='sex',lookup_expr='in')
	class Meta:
		model =Profile
		fields=['sex','city','role','bday']
