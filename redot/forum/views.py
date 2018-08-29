# -*-coding:utf-8-*-
from django.shortcuts import render
from django.http import HttpResponse
import json
# from django.core import serializers
from forum.blocks import boardclass, topicclass, utily
from forum.models import ForumBoard, ForumTopic

# Create your views here.


def index(request):
    top_forumboard_nodes = ForumBoard.objects.filter(parent_board__isnull=True)
    params = {
        'top_forumboard_nodes': top_forumboard_nodes,
    }
    return render(request, 'forum/index.html', params)


def query_from_board_tree_node(request):
    dicts = dict()
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"

    if request.POST:
        dbid = request.POST['dbid']
        boards = ForumBoard.objects.filter(parent_board=dbid)
        if len(boards) == 0:
            dicts['status'] = 'is_leaf'

            topiclist = []
            topics = ForumTopic.objects.filter(board=dbid)
            for topic in topics:
                ztopic = dict()
                ztopic['title'] = topic.title
                ztopic['author'] = topic.author.userprofile.nickname
                ztopic['access_count'] = topic.access_count
                ztopic['reply_count'] = topicclass.topic_get_reply_count(topic)
                # ztopic['created_at'] = serializers.serialize('json', topic.created_at)
                ztopic['created_at'] = utily.json_encoder(topic.created_at)
                topiclist.append(ztopic)

            dicts['topics'] = topiclist
            dicts['nav_items'] = topicclass.TopicsNavItems.items
            dicts['header'] = topicclass.TopicsTableHeader.header
        else:
            dicts['status'] = 'is_not_leaf'

            lst = []
            for board in boards:
                data = dict()
                data['name'] = board.name
                data['brief'] = board.description
                idlst, namelst = boardclass.board_get_managers(board)
                data['manager'] = namelst
                data['user_count'] = str(boardclass.board_get_users_count(board))
                data['hot_total'] = str(boardclass.board_get_hot_topics_count(board)) + '/' +\
                                    str(boardclass.board_get_total_topics_count(board))
                lst.append(data)

            dicts['data'] = lst
            dicts['header'] = boardclass.BoardsTableHeader.header

    response.write(json.dumps(dicts))
    return response
