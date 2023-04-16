function update_status(global_info) {
    document.getElementById('batch_date').innerText=global_info['batch_date']
    let batch_status = global_info['batch_state']
    batch_status_container = document.getElementById('batch_status')
    if(batch_status == 'NOT'){
        batch_status_container.innerText='未开始'
    }else if(batch_status == 'START'){
        batch_status_container.innerText='运行中'
    }else if(batch_status == 'PAUSE'){
        batch_status_container.innerText='暂停中'
    }else if(batch_status == 'STOP'){
        batch_status_container.innerText='已暂停'
    }else if(batch_status == 'SUCCESS'){
        batch_status_container.innerText='已结束'
    }else {
        batch_status_container.innerText='未知'
    }

}

function stop_batch() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET",'http://127.0.0.1:5000/stop_batch');
    xhr.send();
    xhr.onload = function () {
        content = xhr.responseText;
        if (content == 'Y'){
            container = document.querySelector("#batch_status")
            container.innerHTML='暂停中'
        }
    }
}

function start_batch() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET",'http://127.0.0.1:5000/start_batch');
    xhr.send();
    xhr.onload = function () {
        content = xhr.responseText;
        if (content == 'Y'){
            container = document.querySelector("#batch_status")
            container.innerHTML='运行中'
        }
    }
}
function change_batch_date() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET",'http://127.0.0.1:5000/change_batch_date');
    xhr.send();
    xhr.onload = function () {

    }
}

function run_jobs() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET",'http://127.0.0.1:5000/run_jobs');
    xhr.send();
    xhr.onload = function () {
    }
}