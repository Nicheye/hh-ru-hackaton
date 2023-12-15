from django.contrib import admin

# Register your models here.
from .models import User
from .models import Profile
from .models import Event
from .models import InEvent
admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Event)
admin.site.register(InEvent)