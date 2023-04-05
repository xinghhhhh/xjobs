
function all_job(){
    var a_job=document.getElementById('all_job');
    var t_job=document.getElementById('today_job');
    document.getElementById('a_page').style.backgroundColor='lightblue';
    document.getElementById('t_page').style.backgroundColor='transparent';
    a_job.style.display='block';
    t_job.style.display='none';
}

function today_job(){
    var a_job=document.getElementById('all_job');
    var t_job=document.getElementById('today_job');
    document.getElementById('t_page').style.backgroundColor='lightblue';
    document.getElementById('a_page').style.backgroundColor='transparent';
    a_job.style.display='none';
    t_job.style.display='block';
}

//前端获取后台数据并呈现在<div class="ui-tab">中
function information_display_all(page) {
    const informationDisplay = document.querySelector(".ui-tab-all");
    var begin =page*10-10;
    var end = 0;
    if (page*10 < all_count){
        var end = page*10-1;
    }else {
        var end = all_count-1;
    };
    var innerHT = '<table id="container" style="table-layout: fixed;background-color: #bdc3c7" ' +
        '<thead id="a_thead" style="font-size: 18px"> <tr> <td >任务名('+all_count+')</td><td style="width: 80px;text-align: center">类型</td> </tr> </thead> ' +
        '<tbody id="a_tbody" style="background-color: #ecf0f1;font-size: 14px">';
    for (var i=begin;i<=end;i++){
        innerHT +='<tr ><td >';
        innerHT += all_jobs[i][0];
        innerHT +='</td><td style="text-align: center">';
        innerHT += all_jobs[i][1];
        innerHT +='</td></tr>';
    };
    innerHT += '</tbody> </table>';
    informationDisplay.innerHTML = innerHT;
}

function information_display_today(page) {
    const informationDisplay = document.querySelector(".ui-tab-today");
    var begin =page*10-10;
    var end = 0;
    if (page*10 < today_count){
        var end = page*10-1;
    }else {
        var end = today_count-1;
    };
    var innerHT = '<table id="container" style="table-layout: fixed;background-color: #bdc3c7" ' +
        '<thead id="t_thead" style="font-size: 18px"> <tr> <td >任务名('+today_count+')</td><td style="width: 80px;text-align: center">状态</td> </tr> </thead> ' +
        '<tbody id="t_tbody" style="background-color: #ecf0f1;font-size: 14px">';
    for (var i=begin;i<=end;i++){
        innerHT +='<tr ><td >';
        innerHT += today_jobs[i][0];
        innerHT +='</td><td style="text-align: center">';
        innerHT += today_jobs[i][1];
        innerHT +='</td></tr>';
    };
    innerHT += '</tbody> </table>';
    informationDisplay.innerHTML = innerHT;
}






function highlight_all(){
    var trs = document.querySelector('#a_tbody').querySelectorAll("tr");
// 2. 利用循环绑定注册事件
    for (var i = 0; i < trs.length; i++) {
        // 3. 鼠标经过事件 onmouseover 当鼠标经过的时候
        // 给表格添加一个背景属性
        trs[i].onmouseover = function() {
                this.className = 'bg';
            }
            // 4. 鼠标离开事件 onmouseout
        trs[i].onmouseout = function() {
            this.className = '';
        }
        trs[i].onclick = function (){
            alert("ffffffffffffffff")
        }
    }
}

function highlight_today(){
    var trs = document.querySelector('#t_tbody').querySelectorAll("tr");
// 2. 利用循环绑定注册事件
    for (var i = 0; i < trs.length; i++) {
        // 3. 鼠标经过事件 onmouseover 当鼠标经过的时候
        // 给表格添加一个背景属性
        trs[i].onmouseover = function() {
                this.className = 'bg';
            }
            // 4. 鼠标离开事件 onmouseout
        trs[i].onmouseout = function() {
            this.className = '';
        }
        trs[i].onclick = function (){
            alert("yyyyyyyyyyyyyyyyyyyy")
        }
    }
}




//上一页、下一页，首页和尾页的单击触发事件
function page_click_all(item) {
    console.log(item);
    let pageNumber=0;
    if (item.className == "firstPage"){
        console.log(item.className);
        //pageNumber = document.querySelector(".currentPage").value;
        document.querySelector(".currentPage").value=1;
        information_display_all(1)
    }
    else if (item.className == "beforePage") {
        console.log(item.className);
        pageNumber = document.querySelector(".currentPage").value;
        if (pageNumber > 1) {
            document.querySelector(".currentPage").value=Number(pageNumber)-1;
            information_display_all(Number(pageNumber)-1)
        }
    }
    else if (item.className == "nextPage") {
        console.log(item.className);
        pageNumber = document.querySelector(".currentPage").value;
        console.log(pageNumber);
        console.log(typeof(pageNumber));
        if (pageNumber < totalPage) {
            let n=document.querySelector(".currentPage").value=Number(pageNumber)+1;
            information_display_all(Number(pageNumber)+1)
        }
    }
    else {
        console.log(item.className);
        document.querySelector(".currentPage").value=totalPage;
        information_display_all(totalPage)
    };
    highlight_all()
}

function page_click_today(item) {
    console.log(item);
    let pageNumber=0;
    if (item.className == "firstPage"){
        console.log(item.className);
        //pageNumber = document.querySelector(".currentPage").value;
        document.querySelector(".currentPage_today").value=1;
        information_display_today(1)
    }
    else if (item.className == "beforePage") {
        console.log(item.className);
        pageNumber = document.querySelector(".currentPage_today").value;
        if (pageNumber > 1) {
            document.querySelector(".currentPage_today").value=Number(pageNumber)-1;
            information_display_today(Number(pageNumber)-1)
        }
    }
    else if (item.className == "nextPage") {
        console.log(item.className);
        pageNumber = document.querySelector(".currentPage_today").value;
        console.log(pageNumber);
        console.log(typeof(pageNumber));
        if (pageNumber < today_Page) {
            let n=document.querySelector(".currentPage_today").value=Number(pageNumber)+1;
            information_display_today(Number(pageNumber)+1)
        }
    }
    else {
        console.log(item.className);
        document.querySelector(".currentPage_today").value=today_Page;
        information_display_today(today_Page)
    };
    highlight_today()
}
