const form = document.querySelector('.form-container form');
const inputs = document.querySelectorAll('.form-container form input');


// form.addEventListener('submit', (e) => {
//     e.preventDefault();
//     inputs.forEach((input) => {     
//         if (!input.value) {  //input값이 없으면 error 추가
//             input.parentElement.classList.add('error');
//         } else {
//             input.parentElement.classList.remove('error');
//             if(input.type == 'email'){
//                 if(validateEmail(input.value)){
//                     input.parentElement.classList.remove('error');
//                 } else {
//                     input.parentElement.classList.add('error');
//                 }
//             }
//         }
//     });
// });

// function validateEmail(email) {
//     var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
//     return re.test(email);
// }


// 에러 메세지 
if (document.getElementById("error1").innerText) {
    let err = document.getElementById("username");
    err.parentElement.classList.add('error');
}
if (document.getElementById("error2").innerText) {
    let err = document.getElementById("email");
    err.parentElement.classList.add('error');
}
if (document.getElementById("error3").innerText) {
    let err = document.getElementById("password1");
    err.parentElement.classList.add('error');
}
if (document.getElementById("error4").innerText) {
    let err = document.getElementById("password2");
    err.parentElement.classList.add('error');
}

 
function is_checked() {
    const checkbox = document.getElementById('age');
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
function checkSelectAll()  {
    const checkboxes = document.querySelectorAll('input[name="option"]');
    const checked = document.querySelectorAll('input[name="option"]:checked');
    const selectAll = document.querySelector('input[name="selectall"]');

    if(checkboxes.length === checked.length)  {
        selectAll.checked = true;
    } else {
        selectAll.checked = false;
    }
    
}

function selectAll(selectAll)  {
    const checkboxes = document.getElementsByName('option');

    checkboxes.forEach((checkbox) => {
       checkbox.checked = selectAll.checked
    })
    const checkbox = document.getElementById('age');
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

function is_checked() {
    const checkbox = document.getElementById('age');
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


