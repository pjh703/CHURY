const modal = document.querySelector('.modal-inner')
const modal_background = document.querySelector('.overlay')

function close(){
    modal.classList.remove('show-modal');
    modal_background.classList.remove('show-modal');
}
function open(){
    modal.classList.add('show-modal')
    modal_background.classList.add('show-modal')
    }

//Show modal
document.querySelector('.otherbtn').addEventListener('click', () => {
    open()
})

//Hide modal
document.querySelector('#close').addEventListener('click', () => {
    close()
})

document.addEventListener('keyup', function(e) {
    if (e.keyCode == 27) {
        close();
    }
});

window.addEventListener('click', (e) => {
    e.target === modal_background ?  close() : false
})