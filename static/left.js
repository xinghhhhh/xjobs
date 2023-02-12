
function all_job(){
    var a_job=document.getElementById('all_job');
    var t_job=document.getElementById('today_job');
    var r_job=document.getElementById('running_job');
    document.getElementById('a_page').style.backgroundColor='lightblue';
    document.getElementById('t_page').style.backgroundColor='transparent';
    document.getElementById('r_page').style.backgroundColor='transparent';
    //a_job.style.backgroundColor='lightblue';
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
    //t_job.style.backgroundColor='lightblue';
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
    //r_job.style.backgroundColor='lightblue';
    a_job.style.display='none';
    t_job.style.display='none';
    r_job.style.display='block';
}

