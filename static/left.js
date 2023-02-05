let totalPage = 10; //一共多少页
//前端获取后台数据并呈现在<div class="ui-tab">中
function information_display(page=1) {
    const informationDisplay = document.querySelector(".ui-tab");
    informationDisplay.append("dasdsad")
    informationDisplay.innerHTML = 'sadasd <br>  sadasdasasf====<br>'
}

//初始化页面加载
window.onload = function () {
}
//上一页、下一页，首页和尾页的单击触发事件
function page_click(item) {
    console.log(item);
    let pageNumber=0;
    //首页
    if (item.className == "firstPage"){
        console.log(item.className);
        //pageNumber = document.querySelector(".currentPage").value;
        document.querySelector(".currentPage").value=1;
        information_display(1)
    }
    //上一页
    else if (item.className == "beforePage") {
        console.log(item.className);
        pageNumber = document.querySelector(".currentPage").value;
        if (pageNumber > 1) {
            document.querySelector(".currentPage").value=Number(pageNumber)-1;
            information_display(Number(pageNumber)-1)
        }
        // else {
        //     document.querySelector(".beforePage").disabled="false";
        // }
    }
    //下一页
    else if (item.className == "nextPage") {
        console.log(item.className);
        pageNumber = document.querySelector(".currentPage").value;
        console.log(pageNumber);
        console.log(typeof(pageNumber));
        if (pageNumber < totalPage) {
            let n=document.querySelector(".currentPage").value=Number(pageNumber)+1;
            information_display(Number(pageNumber)+1)
        }
        // else {
        //     document.querySelector(".nextPage").disabled="false";
        // }
    }
    //尾页
    else {
        console.log(item.className);
        //pageNumber = document.querySelector(".currentPage").value;
        document.querySelector(".currentPage").value=totalPage;
        information_display(totalPage)
    }
}

function all_job(){
    var a_job=document.getElementById('all_job');
    var t_job=document.getElementById('today_job');
    var r_job=document.getElementById('running_job');
    document.getElementById('a_page').style.backgroundColor='lightblue';
    document.getElementById('t_page').style.backgroundColor='transparent';
    document.getElementById('r_page').style.backgroundColor='transparent';
    a_job.style.backgroundColor='lightblue';
    a_job.style.display='block';
    t_job.style.display='none';
    r_job.style.display='none';
}

function today_job(){
    var a_job=document.getElementById('all_job');
    var t_job=document.getElementById('today_job');
    var r_job=document.getElementById('running_job');
    document.getElementById('t_page').style.backgroundColor='lightblue';
    document.getElementById('a_page').style.backgroundColor='transparent';
    document.getElementById('r_page').style.backgroundColor='transparent';
    t_job.style.backgroundColor='lightblue';
    a_job.style.display='none';
    t_job.style.display='block';
    r_job.style.display='none';
}

function running_job(){
    var a_job=document.getElementById('all_job');
    var t_job=document.getElementById('today_job');
    var r_job=document.getElementById('running_job');
    document.getElementById('r_page').style.backgroundColor='lightblue';
    document.getElementById('a_page').style.backgroundColor='transparent';
    document.getElementById('t_page').style.backgroundColor='transparent';
    r_job.style.backgroundColor='lightblue';
    a_job.style.display='none';
    t_job.style.display='none';
    r_job.style.display='block';
}

