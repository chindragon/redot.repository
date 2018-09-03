from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from forum import models

# Register your models here.


class ProfileInline(admin.StackedInline):
    model = models.UserProfile
    max_num = 1
    can_delete = False


class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline, ]


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)

admin.site.register(models.ForumBoard)
admin.site.register(models.ForumTopic)
admin.site.register(models.ForumMessage)
admin.site.register(models.ForumBoardsMappedUsers)
