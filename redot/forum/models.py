# -*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User
# from django.db.models import signals

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='用户', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=16, default='', blank=False)
    phone = models.CharField(max_length=16, default='', blank=True)
    sex = models.CharField(max_length=8, choices=[('male', '男性'), ('female', '女性'), ('None', '中性')], default='male')

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "更多信息"
        verbose_name_plural = verbose_name
        managed = True
        db_table = 'userprofile'


""""
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

# 不能注册这个函数，否则在添加用户是会出现错误
# signals.post_save.connect(create_user_profile, sender=User) 
"""


class ForumBoard(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256, blank=True, null=True)
    parent_board = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "论坛板块"
        verbose_name_plural = verbose_name
        managed = True
        db_table = 'forum_board'


class ForumTopic(models.Model):
    title = models.CharField(max_length=64, blank=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(User, models.DO_NOTHING)
    board = models.ForeignKey('ForumBoard', models.DO_NOTHING)
    created_at = models.DateTimeField()
    modify_at = models.DateTimeField(blank=True, null=True)
    last_access_at = models.DateTimeField(blank=True, null=True)
    access_count = models.IntegerField()
    stamps = models.FloatField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "主题"
        verbose_name_plural = verbose_name
        managed = True
        db_table = 'forum_topic'


class ForumMessage(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, models.DO_NOTHING)
    board = models.ForeignKey('ForumBoard', models.DO_NOTHING)
    topic = models.ForeignKey('ForumTopic', models.DO_NOTHING)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    modify_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.content[0: 9]

    class Meta:
        verbose_name = "消息"
        verbose_name_plural = verbose_name
        managed = True
        db_table = 'forum_message'


class ForumBoardsMappedUsers(models.Model):
    board = models.ForeignKey('ForumBoard', models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)

    def __str__(self):
        return 'bid' + str(self.board_id) + 'uid' + str(self.user_id)

    class Meta:
        verbose_name = "板块用户映射"
        verbose_name_plural = verbose_name
        managed = True
        db_table = 'forum_boards_mapped_users'
