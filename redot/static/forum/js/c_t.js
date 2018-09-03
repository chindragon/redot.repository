/**
 * 这个文件主要用来动态创建一个完整的表格
 * 第一种：动态创建表格的方式，使用拼接html的方式 （推荐）
 * @param
 * @returns redot.yuxj
 */
/*
    <table class="table table-hover table-bordered table-striped">
        <thead>
            <tr>
                <th class="text-center">编号</th>
                <th class="text-center">名称</th>
                <th class="text-center">简介</th>
                <th class="text-center">版主</th>
                <th class="text-center">子版数量</th>
                <th class="text-center">热帖/总贴</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">1</td>
                <td class="text-center">汽车论坛</td>
                <td class="text-center">支持国产做大做强</td>
                <td class="text-center">余宇</td>
                <td class="text-center">4</td>
                <td class="text-center">1678/18569</td>
            </tr>
            <tr>
                <td class="text-center">2</td>
                <td class="text-center">财经论坛</td>
                <td class="text-center">关乎大家的钱袋子</td>
                <td class="text-center">余宇</td>
                <td class="text-center">1</td>
                <td class="text-center">305/3856</td>
            </tr>
        </tbody>
    </table>
 */

function boards_table_header(header) {
    var html = "";

    html += "<thead>";
    html += "<tr>";
    html += "<th class=\"text-center\">" + header['no'] + "</th>";
    html += "<th class=\"text-center\">" + header['name'] + "</th>";
    html += "<th class=\"text-center\">" + header['brief'] + "</th>";
    html += "<th class=\"text-center\">" + header['manager'] + "</th>";
    html += "<th class=\"text-center\">" + header['user_count'] + "</th>";
    html += "<th class=\"text-center\">" + header['hot_total'] + "</th>";
    html += "</tr>";
    html += "</thead>";

    return html;
}

function boards_table_body(data) {
    var html = "", n = 0;

    html += "<tbody>";
    for(var i = 0; i < data.length; i++)
    {
        n = Number(i) + Number(1);
        html += "<tr>";
        html += "<td class=\"text-center\">" + n + "</td>";
        html += "<td class=\"text-center\">" + data[i]["name"] + "</td>";
        html += "<td class=\"text-center\">" + data[i]["brief"] + "</td>";

        html += "<td class=\"text-center\">";
        var lst = data[i]["manager"];
        for( var k = 0; k < lst.length; k++)
            html += lst[k] + ",";
        html += "</td>";

        html += "<td class=\"text-center\">" + data[i]["user_count"] + "</td>";
        html += "<td class=\"text-center\">" + data[i]["hot_total"] + "</td>";
        html += "</tr>";
    }
    html += "</tbody>";

    return html;
}

function boards_table(header, data) {
    var html = "";

    html += "<table class=\"table table-hover table-bordered table-striped\">";
    html += boards_table_header(header);
    html += boards_table_body(data);
    html += "</table>";

    return html;
}

function topics_table_header(header) {
    var html = "";

    html += "<thead>";
    html += "<tr>";
    html += "<th class=\"text-center\">" + header['title'] + "</th>";
    html += "<th class=\"text-center\">" + header['author'] + "</th>";
    html += "<th class=\"text-center\">" + header['access_count'] + "</th>";
    html += "<th class=\"text-center\">" + header['reply_count'] + "</th>";
    html += "<th class=\"text-center\">" + header['created_at'] + "</th>";
    html += "</tr>";
    html += "</thead>";

    return html;
}


function topics_table_body(data) {
    var html = "", n = 0;

    html += "<tbody>";
    for(var i = 0; i < data.length; i++)
    {
        html += "<tr>";
        html += "<td class=\"text-center\">" + data[i]["title"] + "</td>";
        html += "<td class=\"text-center\">" + data[i]["author"] + "</td>";
        html += "<td class=\"text-center\">" + data[i]['access_count'] + "</td>";
        html += "<td class=\"text-center\">" + data[i]["reply_count"] + "</td>";
        html += "<td class=\"text-center\">" + data[i]["created_at"] + "</td>";
        html += "</tr>";
    }
    html += "</tbody>";

    return html;
}


function topics_table(header, data) {
    var html = "";

    html += "<table class=\"table table-hover table-bordered table-striped\">";
    html += topics_table_header(header);
    html += topics_table_body(data);
    html += "</table>";

    return html;
}