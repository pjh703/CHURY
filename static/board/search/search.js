
// // 계란 이미지 변경

var tab = document.querySelectorAll(".egg-imgs");
var points = document.getElementsByClassName("point");
// for(i = 0;i < 10; i++){
//     console.log(points[i].innerText)
// }
for(i=0;i<10;i++){
    // console.log(parseInt((points[i].innerText).substr(0,2)));
    if (parseInt((points[i].innerText).substr(0,2)) == 5){
        //점수가 9점 이상인 경우
        points[i].innerHTML = "<img src='http://127.0.0.1:8000/static/board/detail/image/5.svg' style='width: 50px; height: 50px; float: left; positon: relative;'><div style='float: left; margin-left: 20px; margin-top: 8px; font-size: 24px;'>" + points[i].innerText + "</div>";
    } else if (parseInt((points[i].innerText).substr(0,2)) == 4) {
        // 점수가 5점 이상인 경우
        points[i].innerHTML = "<img src='http://127.0.0.1:8000/static/board/detail/image/4.svg' style='width: 50px; height: 50px; float: left; positon: relative;'><div style='float: left; margin-left: 20px; margin-top: 8px; font-size: 24px;'>" + points[i].innerText + "</div>";
    } else if (parseInt((points[i].innerText).substr(0,2)) == 3) {
        // 점수가 2점 이상인 경우
        points[i].innerHTML = "<img src='http://127.0.0.1:8000/static/board/detail/image/3.svg' style='width: 50px; height: 50px; float: left; positon: relative;'><div style='float: left; margin-left: 20px; margin-top: 8px; font-size: 24px;'>" + points[i].innerText + "</div>";
    } else if (parseInt((points[i].innerText).substr(0,2)) == 2) {
        // 점수가 0점 이상인 경우
        points[i].innerHTML = "<img src='http://127.0.0.1:8000/static/board/detail/image/2.svg' style='width: 50px; height: 50px; float: left; positon: relative;'><div style='float: left; margin-left: 20px; margin-top: 8px; font-size: 24px;'>" + points[i].innerText + "</div>";
    } else {
        points[i].innerHTML = "<img src='http://127.0.0.1:8000/static/board/detail/image/1.svg' style='width: 50px; height: 50px; float: left; positon: relative;'><div style='float: left; margin-left: 20px; margin-top: 8px; font-size: 24px;'>" + points[i].innerText + "</div>";
    }
}


// pagination
let link = document.getElementsByClassName("numb");
    let currentValue = 1;
    function activeLink(page){
        for(l of link){
            l.classList.remove("active");
        }
        event.target.classList.add("active");
        currentValue = event.target.value;
        document.getElementById('search_page_num').value = page;
        document.getElementById('searchForm').submit();
    }   

    function backBtn2(){
        if(currentValue > 1) {
            for(l of link){
            l.classList.remove("active");
            }
            currentValue=1;
            link[0].classList.add("active");
        }
    }

    function backBtn(){
        if(currentValue > 1) {
            for(l of link){
            l.classList.remove("active");
            }
            currentValue--;
            link[currentValue-1].classList.add("active");
        }
    }

    function nextBtn(){
        if(currentValue < 10) {
            for(l of link){
            l.classList.remove("active");
            }
            currentValue++;
            link[currentValue-1].classList.add("active");
        }
    }

    function nextBtn2(){
        if(currentValue < 10) {
            for(l of link){
            l.classList.remove("active");
            }
            currentValue=link.length;
            link[link.length-1].classList.add("active");
        }
    }

    // -------------------------------------------


// // 계란 이미지 변경

// var tab = document.querySelectorAll(".egg-imgs");
// var points = document.getElementsByClassName("point");
// // for(i = 0;i < 10; i++){
// //     console.log(points[i].innerText)
// // }
// for(i=0;i<10;i++){
//     // console.log(parseInt((points[i].innerText).substr(0,2)));
//     if (parseInt((points[i].innerText).substr(0,2)) >=9){
//         //점수가 9점 이상인 경우
//         points[i].innerHTML = "<img src='http://127.0.0.1:8000/static/board/detail/image/2.svg' style='width: 50px; height: 50px; float: left; positon: relative;'><div style='float: left; margin-left: 20px; margin-top: 10px; font-size: 18px;'>" + points[i].innerText + "</div>";
//     } else if (parseInt((points[i].innerText).substr(0,2)) >=5) {
//         // 점수가 5점 이상인 경우
//         points[i].innerHTML = "<img src='http://127.0.0.1:8000/static/board/detail/image/1.svg' style='width: 50px; height: 50px; float: left; positon: relative;'><div style='float: left; margin-left: 20px; margin-top: 10px; font-size: 18px;'>" + points[i].innerText + "</div>";
//     } else if (parseInt((points[i].innerText).substr(0,2)) >=2) {
//         // 점수가 2점 이상인 경우
//         points[i].innerHTML = "<img src='http://127.0.0.1:8000/static/board/detail/image/3.svg' style='width: 50px; height: 50px; float: left; positon: relative;'><div style='float: left; margin-left: 20px; margin-top: 10px; font-size: 18px;'>" + points[i].innerText + "</div>";
//     } else if (parseInt((points[i].innerText).substr(0,2)) >=0) {
//         // 점수가 0점 이상인 경우
//         points[i].innerHTML = "<img src='http://127.0.0.1:8000/static/board/detail/image/4.svg' style='width: 50px; height: 50px; float: left; positon: relative;'><div style='float: left; margin-left: 20px; margin-top: 10px; font-size: 18px;'>" + points[i].innerText + "</div>";
//     } else {
//         points[i].innerHTML = "<img src='http://127.0.0.1:8000/static/board/detail/image/4.svg' style='width: 50px; height: 50px; float: left; positon: relative;'><div style='float: left; margin-left: 20px; margin-top: 10px; font-size: 18px;'>" + points[i].innerText + "</div>";
//     }
// }

// 페이지네이션 ----
window.onload = function() {
    // 페이징에 사용한 모든 a 태그를 가져와서 변수에 저장
    let a_list = document.getElementsByClassName('page-link');

    // 위 a 태그를 반복하면서 클릭 이벤트를 적용
    Array.from(a_list).forEach(function(e) {
        e.addEventListener('click', function() {
            alert('!');
            // a 태그에 클릭이 발생하면, a 태그에 작성된 data-page속성 값을 input type hidden에 저장
            document.getElementById('page').value = this.dataset.page

            // 검색 양식을 제출해서 뷰로 전달
            document.getElementById('searchForm').submit();
        });
    });
}
