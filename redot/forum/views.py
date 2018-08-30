# -*-coding:utf-8-*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json
from forum.blocks import boardclass, topicclass, utily
from forum.models import ForumBoard, ForumTopic

# Create your views here.


def user_login(request):
    """
    登录输入页面
    """
    return render(request, 'forum/login.html')


def confirm_user_login(request):
    """
    登录验证，并跳转到合适的页面
    """
    request.encoding = 'utf-8'
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return index(request)
            else:
                print("Your account has been disabled!")

    return user_login(request)


def user_logout(request):
    """
    退出登录
    """
    auth.logout(request)
    return index(request)


# @login_required(login_url='/login')
def index(request):
    """
    首页
    """
    params = dict()

    top_forumboard_nodes = ForumBoard.objects.filter(parent_board__isnull=True)
    params['top_forumboard_nodes'] = top_forumboard_nodes
    if request.user.is_authenticated:
        params['islogin'] = True
        params['username'] = request.user.userprofile.nickname
    else:
        params['islogin'] = False

    return render(request, 'forum/index.html', params)


def query_from_board_tree_node(request):
    """
    用户点击树形列表节点时，调整页面显示
    """
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

