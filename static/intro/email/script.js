const form = document.querySelector('.form-container form');
const inputs = document.querySelectorAll('.form-container form input');

form.addEventListener('submit', (e) => {
    e.preventDefault();
    inputs.forEach((input) => {
        if (!input.value) {  //input값이 없으면 error 추가
            input.parentElement.classList.add('error');
        } else {
            input.parentElement.classList.remove('error');
            if(input.type == 'email'){
                if(validateEmail(input.value)){
                    input.parentElement.classList.remove('error');
                } else {
                    input.parentElement.classList.add('error');
                }
            }
        }
    });
});


function validateEmail(email) {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    return re.test(email);
}


// 전체선택 기능
function selectAll(selectAll) {
    const checkboxes
    =
document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach((checkbox) => {
        checkbox.checked = selectAll.checked;
    })
}