# -*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='用户', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=16, default='', blank=False, verbose_name='昵称')
    phone = models.CharField(max_length=16, default='', blank=True, verbose_name='电话')
    sex = models.CharField(max_length=8, choices=[('male', '男性'), ('female', '女性'), ('none', '中性')], default='male',
                           verbose_name='性别')

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "更多信息"
        verbose_name_plural = verbose_name
        managed = True
        db_table = 'userprofile'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        '''
            判断当前user是否有userprofile属性很重要，在管理员认证系统中添加新用户时，
            此属性已经存在，如果在这里再次保存，会因为id冲突而保存失败；但是如果 时用户
            自己写的注册页面，此钩子函数被调用时，userprofile属性 尚不存在，必须创建并
            保存，从而保证数据库的一对一关系成立。
        '''
        if not hasattr(instance, 'userprofile'):
            profile = UserProfile()
            profile.nickname = instance.username  # 保证nickname不为空，会员详情页会允许修改这昵称
            profile.user = instance
            profile.save()
    else:
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()


signals.post_save.connect(create_user_profile, sender=User)


class ForumBoard(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')
    description = models.CharField(max_length=256, blank=True, null=True, verbose_name='描述')
    parent_board = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, verbose_name='父板块')
    is_leaf = models.BooleanField(choices=[(True, '是'), (False, '否')], default=False, verbose_name='是否叶子节点')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "论坛板块"
        verbose_name_plural = verbose_name
        managed = True
        db_table = 'forum_board'


class ForumTopic(models.Model):
    title = models.CharField(max_length=64, blank=True, null=True, verbose_name='标题')
    content = models.TextField(verbose_name='详情')
    author = models.ForeignKey(User, models.DO_NOTHING, verbose_name='作者')
    board = models.ForeignKey('ForumBoard', models.DO_NOTHING, verbose_name='所属板块')
    created_at = models.DateTimeField(verbose_name='创建时间')
    modify_at = models.DateTimeField(blank=True, null=True, verbose_name='修改时间')
    last_access_at = models.DateTimeField(blank=True, null=True, verbose_name='最后访问时间')
    access_count = models.IntegerField(verbose_name='访问次数')
    stamps = models.FloatField(verbose_name='标记信息')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "主题"
        verbose_name_plural = verbose_name
        managed = True
        db_table = 'forum_topic'


class ForumMessage(models.Model):
    content = models.TextField(verbose_name='详情')
    author = models.ForeignKey(User, models.DO_NOTHING, verbose_name='作者')
    board = models.ForeignKey('ForumBoard', models.DO_NOTHING, verbose_name='所属板块')
    topic = models.ForeignKey('ForumTopic', models.DO_NOTHING, verbose_name='所属主题')
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, verbose_name='父信息')
    created_at = models.DateTimeField(verbose_name='创建时间')
    modify_at = models.DateTimeField(blank=True, null=True, verbose_name='修改时间')

    def __str__(self):
        return self.content[0: 9]

    class Meta:
        verbose_name = "消息"
        verbose_name_plural = verbose_name
        managed = True
        db_table = 'forum_message'


class ForumBoardsMappedUsers(models.Model):
    board = models.ForeignKey('ForumBoard', models.DO_NOTHING, verbose_name='板块')
    user = models.ForeignKey(User, models.DO_NOTHING, verbose_name='用户')

    def __str__(self):
        return 'bid' + str(self.board_id) + 'uid' + str(self.user_id)

    class Meta:
        verbose_name = "板块用户映射"
        verbose_name_plural = verbose_name
        managed = True
        db_table = 'forum_boards_mapped_users'
