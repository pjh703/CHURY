const form = document.querySelector('.form-container form');
const inputs = document.querySelectorAll('.form-container form input');


// 에러 메세지
if (document.getElementById("errorpw").innerText) {
    let err = document.getElementById("password1");
    err.parentElement.classList.add('error');
}



function is_checked() {
    const checkbox = document.getElementById('agree');
    const is_checked = checkbox.checked;
    const emailsubmit = document.getElementById('submit');
    if (is_checked) {
        emailsubmit.disabled = false;
        submit.parentElement.classList.remove('submit_disable');
        submit.parentElement.classList.add('submit-hover');
    } else {
        emailsubmit.disabled = true;
        submit.parentElement.classList.add('submit_disable');
        submit.parentElement.classList.remove('submit-hover');
    }
}


// 체크박스 관련
function is_checked() {
    const checkbox = document.getElementById('agree');
    const is_checked = checkbox.checked;
    const emailsubmit = document.getElementById('submit');
    if (is_checked) {
        emailsubmit.disabled = false;
        submit.parentElement.classList.remove('submit_disable');
        submit.parentElement.classList.add('submit-hover');
    } else {
        emailsubmit.disabled = true;
        submit.parentElement.classList.add('submit_disable');
        submit.parentElement.classList.remove('submit-hover');
    }
}

