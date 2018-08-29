# -*-coding:utf-8-*-
from forum import models
from django.contrib.auth.models import Group


class BoardsTableHeader:
    header = {
        'no': '编号',
        'name': '板块',
        'brief': '简介',
        'manager': '版主',
        'user_count': '用户数量',
        'hot_total': '热帖/总贴',
    }

    def __str__(self):
        return self.header


def is_existed_in_list(lst, aid):
    for zid in lst:
        if aid == zid:
            return True

    return False


def board_get_hot_topics_count(board, topiclist=None):
    if topiclist is None:
        topiclist = []

    boards = models.ForumBoard.objects.filter(parent_board=board.id)
    if len(boards) == 0:
        topics = models.ForumTopic.objects.filter(board=board.id)
        for topic in topics:
            if not is_existed_in_list(topiclist, topic.id):
                if topic.stamps > 0:
                    topiclist.append(topic.id)
    else:
        for board in boards:
            board_get_hot_topics_count(board, topiclist)

    return len(topiclist)


def board_get_total_topics_count(board, topiclist=None):
    if topiclist is None:
        topiclist = []

    boards = models.ForumBoard.objects.filter(parent_board=board.id)
    if len(boards) == 0:
        topics = models.ForumTopic.objects.filter(board=board.id)
        for topic in topics:
            if not is_existed_in_list(topiclist, topic.id):
                    topiclist.append(topic.id)
    else:
        for board in boards:
            board_get_total_topics_count(board, topiclist)

    return len(topiclist)


def board_get_users_count(board, usrlist=None):
    if usrlist is None:
        usrlist = []

    boards = models.ForumBoard.objects.filter(parent_board=board.id)
    if len(boards) == 0:
        topics = models.ForumTopic.objects.filter(board=board.id)
        for topic in topics:
            if not is_existed_in_list(usrlist, topic.author.id):
                usrlist.append(topic.author.id)

        messages = models.ForumMessage.objects.filter(board=board.id)
        for message in messages:
            if not is_existed_in_list(usrlist, message.author.id):
                usrlist.append(message.author.id)
    else:
        for board in boards:
            board_get_users_count(board, usrlist)

    return len(usrlist)


def board_get_managers(board, usrlist=None, namelist=None):
    if usrlist is None:
        usrlist = []
    if namelist is None:
        namelist = []

    boards = models.ForumBoard.objects.filter(parent_board=board.id)
    if len(boards) == 0:
        bmus = models.ForumBoardsMappedUsers.objects.filter(board=board.id)
        for bmu in bmus:
            if not is_existed_in_list(usrlist, bmu.user_id):
                user = models.User.objects.get(id=bmu.user_id)
                group = Group.objects.get(name='版主')
                if len(group.user_set.filter(id=user.id)) != 0:
                    usrlist.append(bmu.user_id)
                    namelist.append(user.userprofile.nickname)
    else:
        for board in boards:
            board_get_managers(board, usrlist, namelist)

    return usrlist, namelist

