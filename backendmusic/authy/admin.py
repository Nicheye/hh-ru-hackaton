from django.contrib import admin

# Register your models here.
from .models import User
from .models import Profile
from .models import Event
from .models import InEvent
from .models import EventTag
from .models import Redirection
from .models import EventReact
from .models import Team,TeamPart
admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Event)
admin.site.register(InEvent)
admin.site.register(EventTag)
admin.site.register(Redirection)
admin.site.register(EventReact)
admin.site.register(Team)
admin.site.register(TeamPart)