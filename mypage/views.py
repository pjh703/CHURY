from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView, DetailView

from .forms import UserUpdateForm
from .models import MYBOOK, MYCHOOSE, MYSTAR, MYSELECT
from user.models import MYINFO

from user.models import User, MYINFO
from django.urls import reverse_lazy, reverse
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from pytz import timezone

from konlpy.tag import Okt  # 한글 형태소
import re
from board.views import dataori, cos_sim_df

from sklearn.feature_extraction.text import TfidfVectorizer

from ast import literal_eval
from sklearn.metrics.pairwise import cosine_similarity

from django.core.mail import EmailMessage # 이메일보내기
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives


# 2단계인증 메일보낼때
from django.template.loader import render_to_string
# Create your views here.


data = dataori  



def LibraryView(request, pk):
    sort_type = request.GET.get('sortType')
    # print(sort_type)

    response = []
    id = User.objects.get(id = pk).id
    mybooks = MYBOOK.objects.filter(user_id = id).values('book_id')
    if len(mybooks) > 0:
        for book in mybooks:
            res = data[data['id'] == int(book['book_id'])].to_dict('records')
            if len(res) > 0: 
                response.append(res[0])
                print("response: ", response)
    
        if response != '[]':
            df_response = pd.DataFrame(response)

            genre = np.array(df_response.groupby('장르').count()['id'].index)
            value = np.array(df_response.groupby('장르').count()['id'])
        
            if sort_type == 'title':
                df_response = df_response.sort_values('제목')
            # elif sort_type == 'star':
            #     df_response = df_response.sort_values('제목')
            else:    
                df_response = df_response[::-1]

            lib = df_response.to_dict('records')
                
            context = {
                'response': lib,
                'sortType': sort_type,
                'graph_genre': genre,
                'graph_value': value,

            }
            return render(request, "mypage/library.html", context)
            # return render(request, "mypage/library.html")
    else:
        return render(request, "mypage/library.html")


def LogLock(request, pk):
    if request.method == 'POST' :
        username = pk
        my_email = User.objects.filter(username = pk).values('email')[0]['email']
        email = EmailMessage(
            '[CHURY] 메일인증',                # 제목
            "안녕하세요."
            "\n다음 링크를 누르시면 CHURY 계정의 이메일을 인증하는 화면으로 이동합니다." 
            "\n\nhttp://127.0.0.1:8000/mypage/email_done/" + username +
            "\n\n이메일 인증을 요청하지 않았다면 이 이메일을 무시하셔도 됩니다."
            "\nCHURY와 함께 해주셔서 감사합니다.",
            to=[my_email],  # 받는 이메일 리스트
        )
        email.send()
    return render(request, "mypage/loglock.html")

def EnvView(request):
    return render(request, "mypage/env.html")


def ProfileView(request):
    return render(request, "mypage/profile.html")

def PictureView(request, pk):
    return render(request, "mypage/picture.html")


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
        book_id = request.POST['book_id']
        post.book_id = book_id
        id = request.POST['id']
        post.user = User.objects.get(id=id)      
        post.save()

    # 웹에서 받아온 pk(id)값과 책DB의 id값이 같은 책 데이터를 딕셔너리 형태로 받아옴
    detail_data = data[data['id'] == int(book_id)].to_dict('records')
    # 책에 키워드가 존재하면 keyword에 리스트 형태로 저장
    if len(eval(data[data['id'] == int(book_id)]['keyword'].iloc[0])) > 0:
        keyword = eval(data[data['id'] == int(book_id)]['keyword'].iloc[0])
        # print(keyword)

    # 인트로 유사도 검사 뒤
    book_id3 = book_id

    intro_sim_sorted_idx = cos_sim_df[int(book_id3)].sort_values(ascending=False)[0:11]
    similar_book = data.loc[intro_sim_sorted_idx.index]

    response_intro = similar_book.to_dict('records')[1:6]
    #######


    isbook = False # 책이 있는지 없는지 검사하는 값
    if request.method == "POST":
        id = request.POST['id'] # html form안의 input 태그에서 가져옴 (input태그 id가 id인 경우)
        user_id = User.objects.get(id = id).id # 위와 데이터베이스 같은지 (현재 로그인한 회원과)
        my_book = MYBOOK.objects.filter(user_id = user_id).filter(book_id = book_id) # 위의 상황이 true일때 책 아이디 가져옴.

        star = MYSTAR.objects.filter(user_id=id).filter(book_id=book_id).values('star')

        if len(my_book) > 0:
            isbook = True # 책이 저장되어 있는 경우

        context = {
            'detail_data': detail_data, # 책 정보
            'keyword': keyword, # 책 키워드 리스트
            'isbook': isbook, # 책이 있나없나 true값
            'response_intro' : response_intro, # 유사도검사 인트로
            'star' : star,
        }
        return render(request, "board/detail.html", context)
       
# 삭제
def mydic_del(request):

    if request.method == "POST":
        post = MYBOOK()
        book_id = request.POST['book_id']
        post.book_id = book_id
        id = request.POST['id']
        user_id = User.objects.get(id = id).id
        book = MYBOOK.objects.filter(user_id = user_id).filter(book_id = post.book_id)
        book.delete()

    # 웹에서 받아온 pk(id)값과 책DB의 id값이 같은 책 데이터를 딕셔너리 형태로 받아옴
    detail_data = data[data['id'] == int(book_id)].to_dict('records')
    # 책에 키워드가 존재하면 keyword에 리스트 형태로 저장
    if len(eval(data[data['id'] == int(book_id)]['keyword'].iloc[0])) > 0:
        keyword = eval(data[data['id'] == int(book_id)]['keyword'].iloc[0])
        # print(keyword)

    # 인트로 유사도 검사 뒤
    book_id3 = book_id

    intro_sim_sorted_idx = cos_sim_df[int(book_id3)].sort_values(ascending=False)[0:11]
    similar_book = data.loc[intro_sim_sorted_idx.index]

    response_intro = similar_book.to_dict('records')[1:6]
    #######


    isbook = False # 책이 있는지 없는지 검사하는 값
    if request.method == "POST":
        id = request.POST['id'] # html form안의 input 태그에서 가져옴 (input태그 id가 id인 경우)
        user_id = User.objects.get(id = id).id # 위와 데이터베이스 같은지 (현재 로그인한 회원과)
        my_book = MYBOOK.objects.filter(user_id = user_id).filter(book_id = book_id) # 위의 상황이 true일때 책 아이디 가져옴.

        star = MYSTAR.objects.filter(user_id=id).filter(book_id=book_id).values('star')
        # print(my_book)
        # print(len(my_book))
        # print(star, my_book, pk, book_id)


        if len(my_book) > 0:
            isbook = True # 책이 저장되어 있는 경우

        context = {
            'detail_data': detail_data, # 책 정보
            'keyword': keyword, # 책 키워드 리스트
            'isbook': isbook, # 책이 있나없나 true값
            'response_intro' : response_intro, # 유사도검사 인트로
            'star' : star,
        }
        return render(request, "board/detail.html", context)

# 평점
def mydic2(request):
    if request.method == "POST":
        post = MYSTAR()
        
        book_id = request.POST['book_id']
        # print(book_id)
        star = request.POST['star']
        id = request.POST['id']

        user_id = User.objects.get(id = id).id
        # print('user_id:', user_id)
        before_star = MYSTAR.objects.filter(user_id = user_id).filter(book_id = book_id)
        # print('before_star:',before_star)
        if before_star:
            before_star.delete()

            post.user = User.objects.get(id=id)
            post.book_id = book_id
            post.star = star

            post.save()
        else:
            post.user = User.objects.get(id=id)
            post.book_id = book_id
            post.star = star      

            post.save()

    # 웹에서 받아온 pk(id)값과 책DB의 id값이 같은 책 데이터를 딕셔너리 형태로 받아옴
    detail_data = data[data['id'] == int(book_id)].to_dict('records')
    # 책에 키워드가 존재하면 keyword에 리스트 형태로 저장
    if len(eval(data[data['id'] == int(book_id)]['keyword'].iloc[0])) > 0:
        keyword = eval(data[data['id'] == int(book_id)]['keyword'].iloc[0])
        # print(keyword)

    # 인트로 유사도 검사 뒤
    book_id3 = book_id

    intro_sim_sorted_idx = cos_sim_df[int(book_id3)].sort_values(ascending=False)[0:11]
    similar_book = data.loc[intro_sim_sorted_idx.index]

    response_intro = similar_book.to_dict('records')[1:6]
    #######


    isbook = False # 책이 있는지 없는지 검사하는 값
    if request.method == "POST":
        id = request.POST['id'] # html form안의 input 태그에서 가져옴 (input태그 id가 id인 경우)
        user_id = User.objects.get(id = id).id # 위와 데이터베이스 같은지 (현재 로그인한 회원과)
        my_book = MYBOOK.objects.filter(user_id = user_id).filter(book_id = book_id) # 위의 상황이 true일때 책 아이디 가져옴.

        star = MYSTAR.objects.filter(user_id=id).filter(book_id=book_id).values('star')
 
        if len(my_book) > 0:
            isbook = True # 책이 저장되어 있는 경우

        context = {
            'detail_data': detail_data, # 책 정보
            'keyword': keyword, # 책 키워드 리스트
            'isbook': isbook, # 책이 있나없나 true값
            'response_intro' : response_intro, # 유사도검사 인트로
            'star' : star,
        }
        return render(request, "board/detail.html", context)
             
         
# 선호 장르 선택
def choose(request):

    if request.method == "POST":
        post = MYCHOOSE()
        array = []
        counter = {}
        a = request.POST.getlist('choose')

        for i in range(0,len(a)):
            a_array = a[i].replace(' ', '')
            b_array = a_array.replace('"', '')
            c_array = b_array.replace('[', '')
            d_array = c_array.replace(']', '')
            e_array = d_array.replace("'", '')
            array += e_array.split(',')  # 리스트 형태의 문자열을 가공해서 리스트로
               
        for value in array:    # 리스트에서 장르의 개수 세기
            try: counter[value] += 1
            except: counter[value] = 1



        # 영화 데이터 오버뷰 분석
        overview = request.POST.getlist('overview')
        title = request.POST.getlist('titleview')

        okt = Okt()
        s_word = "아 휴 아이구 아이쿠 아이고 어 나 우리 저희 따라 의해 을 를 에 의 가 으로 로 에게 뿐이다 의거하여 근거하여 입각하여 기준으로 예하면 예를 들면 예를 들자면 저 소인 소생 저희 지말고 하지마 하지마라 다른 물론 또한 그리고 비길수 없다 해서는 안된다 뿐만 아니라 만이 아니다 만은 아니다 막론하고 관계없이 그치지 않다 그러나 그런데 하지만 든간에 논하지 않다 따지지 않다 설사 비록 더라도 아니면 만 못하다 하는 편이 낫다 불문하고 향하여 향해서 향하다 쪽으로 틈타 이용하여 타다 오르다 제외하고 이 외에 이 밖에 하여야 비로소 한다면 몰라도 외에도 이곳 여기 부터 기점으로 따라서 할 생각이다 하려고하다 이리하여 그리하여 그렇게 함으로써 하지만 일때 할때 앞에서 중에서 보는데서 으로써 로써 까지 해야한다 일것이다 반드시 할줄알다 할수있다 할수있어 임에 틀림없다 한다면 등 등등 제 겨우 단지 다만 할뿐 딩동 댕그 대해서 대하여 대하면 훨씬 얼마나 얼마만큼 얼마큼 남짓 여 얼마간 약간 다소 좀 조금 다수 몇 얼마 지만 하물며 또한 그러나 그렇지만 하지만 이외에도 대해 말하자면 뿐이다 다음에 반대로 반대로 말하자면 이와 반대로 바꾸어서 말하면 바꾸어서 한다면 만약 그렇지않으면 까악 툭 딱 삐걱거리다 보드득 비걱거리다 꽈당 응당 해야한다 에 가서 각 각각 여러분 각종 각자 제각기 하도록하다 와 과 그러므로 그래서 고로 한 까닭에 하기 때문에 거니와 이지만 대하여 관하여 관한 과연 실로 아니나다를가 생각한대로 진짜로 한적이있다 하곤하였다 하 하하 허허 아하 거바 와 오 왜 어째서 무엇때문에 어찌 하겠는가 무슨 어디 어느곳 더군다나 하물며 더욱이는 어느때 언제 야 이봐 어이 여보시오 흐흐 흥 휴 헉헉 헐떡헐떡 영차 여차 어기여차 끙끙 아야 앗 아야 콸콸 졸졸 좍좍 뚝뚝 주룩주룩 솨 우르르 그래도 또 그리고 바꾸어말하면 바꾸어말하자면 혹은 혹시 답다 및 그에 따르는 때가 되어 즉 지든지 설령 가령 하더라도 할지라도 일지라도 지든지 몇 거의 하마터면 인젠 이젠 된바에야 된이상 만큼 어찌됏든 그위에 게다가 점에서 보아 비추어 보아 고려하면 하게될것이다 일것이다 비교적 좀 보다더 비하면 시키다 하게하다 할만하다 의해서 연이서 이어서 잇따라 뒤따라 뒤이어 결국 의지하여 기대여 통하여 자마자 더욱더 불구하고 얼마든지 마음대로 주저하지 않고 곧 즉시 바로 당장 하자마자 밖에 안된다 하면된다 그래 그렇지 요컨대 다시 말하자면 바꿔 말하면 즉 구체적으로 말하자면 시작하여 시초에 이상 허 헉 허걱 바와같이 해도좋다 해도된다 게다가 더구나 하물며 와르르 팍 퍽 펄렁 동안 이래 하고있었다 이었다 에서 로부터 까지 예하면 했어요 해요 함께 같이 더불어 마저 마저도 양자 모두 습니다 가까스로 하려고하다 즈음하여 다른 다른 방면으로 해봐요 습니까 했어요 말할것도 없고 무릎쓰고 개의치않고 하는것만 못하다 하는것이 낫다 매 매번 들 모 어느것 어느 로써 갖고말하자면 어디 어느쪽 어느것 어느해 어느 년도 라 해도 언젠가 어떤것 어느것 저기 저쪽 저것 그때 그럼 그러면 요만한걸 그래 그때 저것만큼 그저 이르기까지 할 줄 안다 할 힘이 있다 너 너희 당신 어찌 설마 차라리 할지언정 할지라도 할망정 할지언정 구토하다 게우다 토하다 메쓰겁다 옆사람 퉤 쳇 의거하여 근거하여 의해 따라 힘입어 그 다음 버금 두번째로 기타 첫번째로 나머지는 그중에서 견지에서 형식으로 쓰여 입장에서 위해서 단지 의해되다 하도록시키다 뿐만아니라 반대로 전후 전자 앞의것 잠시 잠깐 하면서 그렇지만 다음에 그러한즉 그런즉 남들 아무거나 어찌하든지 같다 비슷하다 예컨대 이럴정도로 어떻게 만약 만일 위에서 서술한바와같이 인 듯하다 하지 않는다면 만약에 무엇 무슨 어느 어떤 아래윗 조차 한데 그럼에도 불구하고 여전히 심지어 까지도 조차도 하지 않도록 않기 위하여 때 시각 무렵 시간 동안 어때 어떠한 하여금 네 예 우선 누구 누가 알겠는가 아무도 줄은모른다 줄은 몰랏다 하는 김에 겸사겸사 하는바 그런 까닭에 한 이유는 그러니 그러니까 때문에 그 너희 그들 너희들 타인 것 것들 너 위하여 공동으로 동시에 하기 위하여 어찌하여 무엇때문에 붕붕 윙윙 나 우리 엉엉 휘익 윙윙 오호 아하 어쨋든 만 못하다 하기보다는 차라리 하는 편이 낫다 흐흐 놀라다 상대적으로 말하자면 마치 아니라면 쉿 그렇지 않으면 그렇지 않다면 안 그러면 아니었다면 하든지 아니면 이라면 좋아 알았어 하는것도 그만이다 어쩔수 없다 하나 일 일반적으로 일단 한켠으로는 오자마자 이렇게되면 이와같다면 전부 한마디 한항목 근거로 하기에 아울러 하지 않도록 않기 위해서 이르기까지 이 되다 로 인하여 까닭으로 이유만으로 이로 인하여 그래서 이 때문에 그러므로 그런 까닭에 알 수 있다 결론을 낼 수 있다 으로 인하여 있다 어떤것 관계가 있다 관련이 있다 연관되다 어떤것들 에 대해 이리하여 그리하여 여부 하기보다는 하느니 하면 할수록 운운 이러이러하다 하구나 하도다 다시말하면 다음으로 에 있다 에 달려 있다 우리 우리들 오히려 하기는한데 어떻게 어떻해 어찌됏어 어때 어째서 본대로 자 이 이쪽 여기 이것 이번 이렇게말하자면 이런 이러한 이와 같은 요만큼 요만한 것 얼마 안 되는 것 이만큼 이 정도의 이렇게 많은 것 이와 같다 이때 이렇구나 것과 같이 끼익 삐걱 따위 와 같은 사람들 부류의 사람들 왜냐하면 중의하나 오직 오로지 에 한하다 하기만 하면 도착하다 까지 미치다 도달하다 정도에 이르다 할 지경이다 결과에 이르다 관해서는 여러분 하고 있다 한 후 혼자 자기 자기집 자신 우에 종합한것과같이 총적으로 보면 총적으로 말하면 총적으로 대로 하다 으로서 참 그만이다 할 따름이다 쿵 탕탕 쾅쾅 둥둥 봐 봐라 아이야 아니 와아 응 아이 참나 년 월 일 령 영 일 이 삼 사 오 육 륙 칠 팔 구 이천육 이천칠 이천팔 이천구 하나 둘 셋 넷 다섯 여섯 일곱 여덟 아홉 령 영 이 있 하 것 들 그 되 수 이 보 않 없 나 사람 주 아니 등 같 우리 때 년 가 한 지 대하 오 말 일 그렇 위하 때문 그것 두 말하 알 그러나 받 못하 일 그런 또 문제 더 사회 많 그리고 좋 크 따르 중 나오 가지 씨 시키 만들 지금 생각하 그러 속 하나 집 살 모르 적 월 데 자신 안 어떤 내 내 경우 명 생각 시간 그녀 다시 이런 앞 보이 번 나 다른 어떻 여자 개 전 들 사실 이렇 점 싶 말 정도 좀 원 잘 통하 놓 짓 죽 퍼 채 환 회 강 잡 위 장 꿰 걸 퉁 로서 곳 리 왜너 이제 킨 음 거 그게 넌 니 부러 채 테 그동안 게 닌 헤 듯 난 위해 란 컬 보이지 뿐 메 움 듯 대고 은 요 지나 탓 르 다그 루 덥석 네네 드보 이제 트 덩 이건 아예 치 더니 송두리째 뭐 오른 추 척 료 채 세 손 흐 위해 드 카 사드 이자 린느 공저 줄게 다그 닉 휘 페 위 못 건 대한 테 케 걸 어그 늘 다 셈 꼽았다 거 거나 뒤 유 잡 배 임 날 오웰 가빠왔 이마 볼 거 단 서도 곳 가주 게 현 세 민 다린 린 임 안고 고 덤 재 위해 재밋고 하이 다그 다가 로크 1000 렌 체 런지훗 접 솔 위 꺽꺽 뿜어져 패공 이기 최 리자 보시 트라팔가 살로 시피 마루이 욜 다나 스노 한지 뿐 고랑 움 토니 쪽 짝짝 떳 텅 피오네 카 칭했다 록 님꺼 주신 날 번만 나니 흐읏 뭣 함 로서 이후 습 송두리째 그로 사가 깨 거후훗 꼭 볼 척 작 엮 유 차 게 입 곳 모든 듯 티 엘 깨 온 거 머 꽉 공 테 은 르 점점 기 우뚝 끌 빈 막 퍼 뿐 뭘 뭐 헌 듯 윤 탠 덩 치 최 경 간 퇴 거 임 딘 애 킨 요"
        stopword = s_word.split(' ')
              
        overview_word = []
        for i in range(0,len(overview)):  # 영화 시놉시스, 영화 제목에서 형태소 추출하는
        #     word = okt.normalize(i)  # 정규화
            wo = overview[i]
            wt = title[i]
            word_o = re.sub('[^가-힝0-9a-zA-Z\\s]', '', str(wo))  # 영, 한, 숫 아닌 거 제외
            word_t = re.sub('[^가-힝0-9a-zA-Z\\s]', '', str(wt))  # 영, 한, 숫 아닌 거 제외
            
            word_o = okt.nouns(word_o)  # 형태소 추출
            word_t = okt.nouns(word_t)  # 형태소 추출
            
            overview_word += [i for i in word_o if i not in stopword]
            overview_word += [i for i in word_t if i not in stopword]
            
            overview_word = list(set(overview_word))

        movie_word = ''
        for i in overview_word:
            movie_word += i + ' '


        df_list = data['장르'].drop_duplicates().to_list()  # 장르 목록
        data2 = pd.DataFrame(columns=data.columns)

        # 장르별 천개씩
        for i in df_list:
            data2 = pd.concat([data2, data[data['장르'] == i][:1000]])
        
        data2 = data2.reset_index(drop=True)

        # 마지막열에 추가
        data2.loc[len(data2)] = [len(data2),len(data2),len(data2),'mokpyo', '작', '장','커버','키','조','조단','추','추단','인','인단', movie_word,'0','2','3','0','0']

        print(data2.tail)
   
        vectorizer = TfidfVectorizer(min_df = 1000, sublinear_tf = True)
        vectorizerfit = vectorizer.fit(data2['total'])
        vecdf = vectorizer.transform(data2['total']).toarray()

        word_list = sorted(vectorizerfit.vocabulary_.items()) # 단어사전을 정렬합니다.

        # 용이한 시각화를 위하여 데이터프레임 변환
        tf_idf_df = pd.DataFrame(vecdf, columns = word_list, index = data2.제목)
        # 코사인 유사도 계산
        cos_sim_df = pd.DataFrame(cosine_similarity(tf_idf_df, tf_idf_df))
        print(data2.index[(data2['제목'] == 'mokpyo')])
        intro_sim_idx = cos_sim_df[data2.index[data2['제목'] == 'mokpyo'].to_list()[0]]
        intro_sim_sorted_idx = intro_sim_idx.sort_values(ascending=False)[0:21]
        similar_book = data2.loc[intro_sim_sorted_idx.index]


        cols = [k for k in similar_book]
        book_queryset = [dict(zip(cols, k)) for k in similar_book.values]

        print(similar_book)

        # 유사도 검사한 결과 데이터베이스에 저장

        id = request.POST['id']
        
        book_list = []
        for l in range(1,21):
            bulk = book_queryset[l]['id']
            book_list.append(bulk)

        bulk_list = []

        for l in book_list:
            bulk_list.append(MYSELECT(
                            user_id=User.objects.get(id=id).id,
                            book_id=l))
                            
        selete_data = MYSELECT.objects.bulk_create(bulk_list)

        
        context = {
            'selete_data':selete_data,
        }


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
        id = request.POST['id']
        post.user = User.objects.get(id=id)        
        post.save()

    return redirect("/board/home", context)
    

def email_done(request, pk):
    context = {
        'username' : pk
    }
    return render(request, "mypage/email_done.html", context) 

def email_done2(request):
    if request.method == "POST":
        username = request.POST['username']
        try:
            user_id = User.objects.filter(username = username)[0].id
        except:
            return redirect("/board/home")
        
        try:
            post = MYINFO.objects.get(id = user_id)
        except:
            post = MYINFO()
            post.id = user_id
        
        post.email_confirm = 1
        post.email_id = user_id
        post.save()
    
    return render(request, "mypage/email_done2.html")

# 고객지원센터
def notice(request):

    return render(request, "mypage/notice.html")

# 카카오페이 결제
def pay(request):
    if request.method == "POST":
        id = request.POST['user_id']
        user_id = User.objects.get(id = id).id
        try:
            is_regist = MYINFO.objects.get(id = user_id).regist
        except:
            is_regist = 0

        print(is_regist)

        if(is_regist == 1):
            return render(request, 'mypage/profile.html')
        else:
            URL = "https://kapi.kakao.com/v1/payment/ready"
            headers = {
                "Authorization": "KakaoAK " + "8014c7551c26de7bcadcd6419eb22777",   # 변경불가
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
            }
            params = {
                "cid": "TC0ONETIME",    # 테스트용 코드
                "partner_order_id": "1001",     # 주문번호
                "partner_user_id": user_id,    # 유저 아이디
                "item_name": "CHURY 이용권",        # 구매 물품 이름
                "quantity": "1",                # 구매 물품 수량
                "total_amount": "4900",        # 구매 물품 가격
                "tax_free_amount": "0",         # 구매 물품 비과세
                "approval_url": f"http://localhost:8000/mypage/approval/{user_id}/",
                "cancel_url": "http://localhost:8000/mypage/profile/",
                "fail_url": "http://localhost:8000/mypage/profile/",
            }

            res = requests.post(URL, headers=headers, params=params)
            request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
            next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
            return redirect(next_url)
    
    return render(request, 'mypage/env.html')


# 결제 승인
def approval(request, pk):
    user_id = User.objects.get(id = pk).id
    URL = "https://kapi.kakao.com/v1/payment/approve"
    headers = {
        "Authorization": "KakaoAK " + "8014c7551c26de7bcadcd6419eb22777",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",    # 테스트용 코드
        "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": "1001",     # 주문번호
        "partner_user_id": user_id,    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params)
    if(res.status_code == 200):
        try:
            post = MYINFO.objects.get(id = user_id)
        except:
            post = MYINFO()
            post.id = user_id

        post.regist = 1
        post.email_id = user_id
        post.reg_date = datetime.now(timezone('Asia/Seoul'))
        post.save()

    return render(request, 'mypage/profile.html')

