# -*-coding:utf-8-*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json
from forum.blocks import boardclass, topicclass, utily
from forum.models import ForumBoard, ForumTopic

# Create your views here.


def get_user_info_from_request(request, dicts=None):
    if dicts is None:
        dicts = dict()

    dicts['username'] = request.user.username
    dicts['email'] = request.user.email
    dicts['phone'] = request.user.userprofile.phone
    dicts['nickname'] = request.user.userprofile.nickname
    dicts['firstname'] = request.user.first_name
    dicts['secondname'] = request.user.last_name
    if request.user.userprofile.sex == 'male':
        dicts['sex'] = '男性'
    else:
        if request.user.userprofile.sex == 'female':
            dicts['sex'] = '女性'
        else:
            if request.user.userprofile.sex == 'none':
                dicts['sex'] = '中性'
            else:
                dicts['sex'] = ''

    return dicts


def user_register(request):     # 用户注册页面
    auth.logout(request)    # 先登出，再去注册页面
    return render(request, 'forum/register.html')


def user_login(request):    # 登录输入页面
    return render(request, 'forum/login.html')


@login_required(login_url='/login')
def user_info(request):     # 用户信息
    dicts = get_user_info_from_request(request)
    return render(request, 'forum/user_info.html', dicts)


@login_required(login_url='/login')
def user_settings(request):     # 用户设置
    dicts = get_user_info_from_request(request)
    return render(request, 'forum/user_settings.html', dicts)


@login_required(login_url='/login')
def modify_password(request):   # 修改密码
    dicts = {'username': request.user.username}
    return render(request, 'forum/modify_password.html', dicts)


def pop_message(is_success, errors=None, successes=None, tag=None, url=None):
    if tag is None:
        tag = '返回'
    if url is None:
        url = '#'

    response = HttpResponse()
    response['Content-Type'] = "text/html;charset=utf-8"
    response.write("<html>")
    response.write("<p>")

    if not is_success:
        if len(errors) != 0:
            response.write(errors[0])
        else:
            response.write("错误!")
    else:
        if len(successes) != 0:
            response.write(successes[0])
        else:
            response.write("成功!")

    response.write("</p>")
    response.write("<a href='" + url + "' target='_self'>")
    response.write(tag)
    response.write("</a>")
    response.write("</html>")
    response.flush()

    return response


def confirm_user_register(request):     # 验证注册信息，并跳转到合适的页面
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
            if user is None:
                errors.append('注册用户失败，用户名已存在！')

    if len(errors) == 0:
        response = pop_message(True, successes=['注册成功！请登录...'], tag='去登陆', url='login')
    else:
        response = pop_message(False, errors=errors, tag='返回', url='register')
    return response


@login_required(login_url='/login')
def confirm_modify_password(request):   # 验证修改密码
    errors = []
    request.encoding = 'utf-8'
    if request.method == 'POST':
        oldpassword = request.POST.get('oldpassword', None)
        if not oldpassword:
            errors.append('旧密码不能为空 ！')
        newpassword = request.POST.get('newpassword', None)
        if not newpassword:
            errors.append('新密码不能为空！')
        confirmpassword = request.POST.get('confirmpassword', None)
        if not confirmpassword:
            errors.append('确认密码不能为空！')

        user = auth.authenticate(username=request.user.username, password=oldpassword)
        if user is None or (not user.is_active):
                errors.append('旧密码输入错误!')

        if newpassword != confirmpassword:
            errors.append('两次输入的密码不一致！')

    if len(errors) == 0:
        request.user.set_password(newpassword)
        request.user.save()
        response = pop_message(True, successes=['密码修改成功！请重新登录'], tag='去登录', url='login')
    else:
        response = pop_message(False, errors=errors, tag='返回', url='modify_password')
    return response


@login_required(login_url='/login')
def confirm_user_settings(request):     # 验证用户设置的信息
    errors = []
    request.encoding = 'utf-8'
    if request.method == 'POST':
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        nickname = request.POST.get('nickname', None)
        firstname = request.POST.get('firstname', None)
        secondname = request.POST.get('secondname', None)
        sex = request.POST.get('sex', None)

        if email != '':
            request.user.email = email
        if firstname != '':
            request.user.first_name = firstname
        if secondname != '':
            request.user.last_name = secondname
        if hasattr(request.user, 'userprofile'):
            if nickname != '':
                request.user.userprofile.nickname = nickname
            if phone != '':
                request.user.userprofile.phone = phone
            if sex != '':
                if sex.find('男') >= 0:
                    request.user.userprofile.sex = 'male'
                else:
                    if sex.find('女') >= 0:
                        request.user.userprofile.sex = 'female'
                    else:
                        request.user.userprofile.sex = 'none'
        request.user.save()
    else:
        errors.append('设置失败！')

    if len(errors) == 0:
        response = pop_message(True, successes=['设置成功，请重新登录...'], tag='去登录', url='login')
    else:
        response = pop_message(False, errors=errors, tag='返回', url='user_settings')
    return response


def confirm_user_login(request):    # 登录验证，并跳转到合适的页面
    errors = []
    request.encoding = 'utf-8'
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return index(request)
        else:
            errors.append("密码验证失败！")
    else:
        errors.append('登录失败！')

    if len(errors) == 0:
        return index(request)
    else:
        return pop_message(False, errors=errors, tag='返回', url='login')


def user_logout(request):   # 退出登录
    auth.logout(request)
    return index(request)


def index(request):     # 首页
    params = dict()
    top_forumboard_nodes = ForumBoard.objects.filter(parent_board__isnull=True)
    get_branch_data(top_forumboard_nodes, params)
    params['top_forumboard_nodes'] = top_forumboard_nodes
    if request.user.is_authenticated:
        params['islogin'] = True
        params['username'] = request.user.userprofile.nickname
    else:
        params['islogin'] = False

    return render(request, 'forum/index.html', params)


def get_branch_data(boards, dicts=None):
    if dicts is None:
        dicts = dict()

    lst = []
    dicts['status'] = 'is_branch'
    for board in boards:
        data = dict()
        data['name'] = board.name
        data['brief'] = board.description
        idlst, namelst = boardclass.board_get_managers(board)
        data['manager'] = namelst
        data['user_count'] = str(boardclass.board_get_users_count(board))
        data['hot_total'] = str(boardclass.board_get_hot_topics_count(board)) + '/' + \
                            str(boardclass.board_get_total_topics_count(board))
        lst.append(data)

    dicts['data'] = lst
    dicts['header'] = boardclass.BoardsTableHeader.header

    return dicts


def get_leaf_data(dbid, dicts=None):
    if dicts is None:
        dicts = dict()

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

    return dicts


def query_from_board_tree_node(request):    # 用户点击树形列表节点时，调整页面显示
    dicts = dict()
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"

    if request.POST:
        dbid = request.POST['dbid']
        board = ForumBoard.objects.filter(id=dbid).get(id=dbid)
        if board.is_leaf:
            dicts = get_leaf_data(dbid)
        else:
            boards = ForumBoard.objects.filter(parent_board=dbid)
            dicts = get_branch_data(boards)

    response.write(json.dumps(dicts))
    return response

