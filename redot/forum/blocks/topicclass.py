# -*-coding:utf-8-*-
from forum import models
from django.contrib.auth.models import Group


class TopicsNavItems:
    items = {
        'default': '默认',
        'newest': '最新',
        'best': '精品',
        'inner_task': '版务',
        'rank_list': '排行',
        'rank_user': '人物',
        'users': '成员',
        'update': '刷新',
        'new': '发帖',
    }

    def __str__(self):
        return self.items


class TopicsTableHeader:
    header = {
        'title': '标题',
        'author': '作者',
        'access_count': '点击',
        'reply_count': '回复',
        'created_at': '创建时间',
    }

    def __str__(self):
        return self.header


def topic_get_reply_count(topic):
    messages = models.ForumMessage.objects.filter(topic=topic)
    return len(messages)
