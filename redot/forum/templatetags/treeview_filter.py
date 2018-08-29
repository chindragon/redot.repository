# -*-coding:utf-8-*-
__author__ = 'redot.Yu'

from forum.models import ForumBoard
from django import template

register = template.Library()


@register.filter
def get_next_forumboard_nodes(fid):
    return ForumBoard.objects.filter(parent_board=fid)



