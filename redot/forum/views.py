# -*-coding:utf-8-*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
# from django.contrib.auth.decorators import login_required
import json
from forum.blocks import boardclass, topicclass, utily
from forum.models import ForumBoard, ForumTopic

# Create your views here.


def user_register(request):
    """
    用户注册页面
    """
    return render(request, 'forum/register.html')


def user_login(request):
    """
    登录输入页面
    """
    return render(request, 'forum/login.html')


def confirm_user_register_pop_message(errors, response = None):
    if response is None:
        response = HttpResponse()

    response = HttpResponse()
    response['Content-Type'] = "text/html;charset=utf-8"
    response.write("<html>")
    response.write("<p>")

    if len(errors) != 0:
        response.write(errors[0])
        response.write("</p>")
        response.write("<a href='register' target='_self'>")
        response.write("返回")
    else:
        response.write('注册成功，欢迎您!请登录...')
        response.write("</p>")
        response.write("<a href='login' target='_self'>")
        response.write("去登陆")

    response.write("</a>")
    response.write("</html>")
    response.flush()

    return response



def confirm_user_register(request):
    """
    验证注册信息，并跳转到合适的页面
    """
    errors = []
    request.encoding = 'utf-8'
    if request.method == 'POST':
        username = request.POST.get('username', None)
        if not username:
            errors.append('用户名不能为空！')
        password = request.POST.get('password', None)
        if not password:
            errors.append('密码不能为空 ！')
        confirm = request.POST.get('confirm', None)
        if not confirm:
            errors.append('确认密码不能为空！')
        email = request.POST.get('email', None)
        if not email:
            errors.append('邮件不能为空！')

        if password != confirm:
            errors.append('两次输入的密码不一致！')

        if len(errors) == 0:
            user = auth.models.User.objects.create_user(username=username, password=password, email=email)
            b = hasattr(user, 'userprofile')
            if user is None:
                errors.append('注册用户失败，用户名已存在！')

    response = confirm_user_register_pop_message(errors)
    return response


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

