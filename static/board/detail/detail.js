window.alert = function(message, timeout=null){
    const alert = document.createElement('div');
    alert.classList.add('alert');
    // alert.setAttribute('style', '
    //     position:fixed;
    //     top: 50%;
    //     left: 50%
    //     padding: 20px;
    //     border-radius: 10px;
    //     box-shadow: 0 10px 5px 0 #00000044;

    // ');
    alert.innerText = message;
    document.body.appendChild(alert);
}