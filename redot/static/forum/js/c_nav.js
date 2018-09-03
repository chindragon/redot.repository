/**
 * 这个文件主要用来动态创建一个完整的导航栏
 * 第一种：动态创建表格的方式，使用拼接html的方式 （推荐）
 * @param
 * @returns redot.yuxj
 */
/*
    <ul class="nav nav-tabs">
        <li class="active">
             <a href="#">首页</a>
        </li>
        <li class="dropdown pull-left">
            <a href="#" data-toggle="dropdown" class="dropdown-toggle">更多<strong class="caret"></strong></a>
            <ul class="dropdown-menu">
                <li>
                     <a href="#">操作</a>
                </li>
            </ul>
        </li>
        <li class="pull-right">
             <a href="#">首页</a>
        </li>
    </ul>
 */

function topics_nav_left(left) {
    var html = "";

    html += "<li>";
    html += "<a>" + left['default'] + "</a>";
    html += "</li>";

    html += "<li class=\"active\">";
    html += "<a>" + left['newest'] + "</a>";
    html += "</li>";

    html += "<li>";
    html += "<a>" + left['best'] + "</a>";
    html += "</li>";

    return html;
}

function topics_nav_dropdown(dd) {
    var html = "";

    html += "<li class=\"dropdown pull-left\">";
    html += "<a href=\"#\" data-toggle=\"dropdown\" class=\"dropdown-toggle\">更多<strong class=\"caret\"></strong></a>";
    html += "<ul class=\"dropdown-menu\">";

    html += "<li>";
    html += "<a href=\"#\">" + dd['inner_task'] + "</a>";
    html += "</li>";

    html += "<li>";
    html += "<a href=\"#\">" + dd['rank_list'] + "</a>";
    html += "</li>";

    html += "<li>";
    html += "<a href=\"#\">" + dd['rank_user'] + "</a>";
    html += "</li>";

    html += "<li>";
    html += "<a href=\"#\">" + dd['users'] + "</a>";
    html += "</li>";

    html += "</ul>";
    html += "</li>";

    return html;
}

function topics_nav_right(right) {
    var html = "";

    html += "<li class=\"pull-right\">";
    html += "<button class=\"btn btn-default\">" + right['new'] + "</button>";
    html += "</li>";

    html += "<li class=\"pull-right\">";
    html += "<button class=\"btn btn-defult\">" + right['update'] + "</button>";
    html += "</li>";

    return html;
}

function topics_nav(nav, managers) {
    var html = "";

    html += "<ul class=\"nav nav-tabs\">";
    html += topics_nav_left(nav);
    html += topics_nav_dropdown(nav);
    html += topics_nav_right(nav);
    html += "</ul>";

    html += "<h5 class=\"bg-info\">" + "版主:";
    for( var i = 0; i < managers.length; i++){
        if(i != 0){
            html += ",";
        }
        html += managers[i];
    }
    html += "</h5>";

    return html;
}