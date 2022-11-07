var counter=1;
document.getElementById('radio' + counter).checked = true;
let interval = setInterval(banner,4500)
function banner(n){
    if (counter == 4) counter = 0

    document.getElementById('radio' + (counter+1)).checked = true;
    counter++;
}