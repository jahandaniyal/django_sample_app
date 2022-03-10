from django.contrib import admin

from app.models import User, Usage, UsageTypes

admin.site.register(User)
admin.site.register(Usage)
admin.site.register(UsageTypes)