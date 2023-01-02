from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView, DetailView

from .forms import UserUpdateForm
from .models import MYBOOK, MYINFO, MYCHOOSE

from user.models import User
from django.urls import reverse_lazy, reverse
import requests
# Create your views here.



def LibraryView(request, pk):
    response = {}
    response_list = []
    Key = 'ttbsaspower81040001'
    email_id = User.objects.get(username = pk).id
    mydic = MYBOOK.objects.filter(email_id = email_id).values('mydic')
    for i in range(0,len(mydic)):
        mydic_num = mydic[i]['mydic']
        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey={Key}&itemIdType=ISBN13&ItemId={mydic_num}&Cover=Big&output=js&Version=20131101&OptResult=ebookList,usedList,reviewList"
        response_url = requests.get(apiurl).json()
        response_list.append(response_url['item'])
        response['item'] = sum(response_list, [])

    context = {
        'response': response,
    }
    return render(request, "mypage/library.html", context)
    # return render(request, "mypage/library.html")


def LogLock(request):
    return render(request, "mypage/loglock.html")


def EnvView(request):
    return render(request, "mypage/env.html")


def ProfileView(request):
    return render(request, "mypage/profile.html")


# 회원탈퇴
class UserDeleteView(DeleteView):
    model = User
    template_name = 'mypage/delete.html'
    success_url = reverse_lazy('user:login')
    context_object_name = 'user'
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
        

# 회원정보
class UserDetailView(DetailView):
    template_name = 'member/detail.html'
    model = User


# 회원정보 수정
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name',]
    success_url = reverse_lazy('mypage:profile')
    template_name = 'mypage/update.html'


# 비밀번호 변경
class PwUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('user:login')
    template_name = 'mypage/pwupdate.html'



# 내 도서관 추가
def mydic(request):

    if request.method == "POST":
        post = MYBOOK()
        post.mydic = request.POST['mydic']
        email = request.POST['email']
        username = request.POST['username']
        post.email = User.objects.get(email=email)      
        post.save()
    return redirect(f"/mypage/library/{username}")
       
# 삭제
def mydic_del(request):

    if request.method == "POST":
        post = MYBOOK()
        post.mydic = request.POST['mydic']
        email = request.POST['email']
        email_id = User.objects.get(email = email).id
        mydic = MYBOOK.objects.filter(email_id = email_id).filter(mydic = post.mydic)
        mydic.delete()
    return redirect(f"/board/detail/{post.mydic}")

# 평점
def mydic2(request):
    if request.method == "POST":
        post = MYBOOK()
        post.mydic = request.POST['mydic']
        post.myread = request.POST['myread']
        email = request.POST['email']
        post.email = User.objects.get(email=email)      
        post.save()
    return redirect(f"/board/detail/{post.mydic}")
         
         
# 선호 장르 선택
def choose(request):

    if request.method == "POST":
        post = MYCHOOSE()
        abc = []
        array = []
        counter = {}
        a = request.POST.getlist('choose')

        # 불러온 값이 리스트처럼 생긴 str값이라 다시 리스트로
        for i in range(0,len(a)):
            a_array = a[i].replace(' ', '')
            b_array = a_array.replace('"', '')
            c_array = b_array.replace('[', '')
            d_array = c_array.replace(']', '')
            e_array = d_array.replace("'", '')
            array += e_array.split(',')
        
        # counter dict에 {장르 : 갯수} 추가
        for value in array:
            try: counter[value] += 1
            except: counter[value] = 1
        # print(counter)
        # print(counter['액션'])
        # gen_list = ['액션', '모험', '애니메이션', '코미디', '범죄', '다큐멘터리', '드라마', '가족', '판타지', '역사', '공포', '음악', '미스터리', '로맨스', 'SF', 'TV영화', '스릴러', '전쟁', '서부']
        # gen_elist = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'ScienceFiction', 'TVMovie', 'Thriller', 'War', 'Western']
        # for i in range(0, len(gen_list)):
        #     post.gen_elist['{num}'.format(num = i)] = counter[gen_list[i]]
  
        try:
            post.Action =counter['액션']
        except:
            pass
        try:
            post.Adventure =counter['모험']
        except:
            pass
        try:
            post.Animation =counter['애니메이션']
        except:
            pass
        try:
            post.Comedy =counter['코미디']
        except:
            pass
        try:
            post.Crime =counter['범죄']
        except:
            pass
        try:
            post.Documentary =counter['다큐멘터리']
        except:
            pass
        try:
            post.Drama =counter['드라마']
        except:
            pass
        try:
            post.Family =counter['가족']
        except:
            pass
        try:
            post.Fantasy =counter['판타지']
        except:
            pass
        try:
            post.History =counter['역사']
        except:
            pass
        try:
            post.Horror =counter['공포']
        except:
            pass
        try:
            post.Music =counter['음악']
        except:
            pass
        try:
            post.Mystery =counter['미스터리']
        except:
            pass
        try:
            post.Romance =counter['로맨스']
        except:
            pass
        try:
            post.ScienceFiction =counter['SF']
        except:
            pass
        try:
            post.TVMovie =counter['TV영화']
        except:
            pass
        try:
            post.Thriller =counter['스릴러']
        except:
            pass
        try:
            post.War =counter['전쟁']
        except:
            pass
        try:
            post.Western =counter['서부']
        except:
            pass
        email = request.POST['email']
        post.email = User.objects.get(email=email)        
        post.save()
    return redirect("/board/home")
    