from django.contrib.auth.models import Group
from django.contrib import admin
from .models import BookModel, ProfileDataModel

admin.site.unregister(Group)
admin.site.register(BookModel)
admin.site.register(ProfileDataModel)

