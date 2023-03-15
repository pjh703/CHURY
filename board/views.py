import requests

from lib2to3.pgen2.token import DOUBLESTAREQUAL

from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404  

from django.views.generic import DetailView
from user.models import User
from mypage.models import MYBOOK, MYCHOOSE, MYSTAR, COMMENT, MYSELECT
from xlrd import open_workbook
from django.core.paginator import Paginator  

import numpy as np
import pandas as pd
import math

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval

from konlpy.tag import Okt

# 글자료 불러오기
dataori = pd.read_excel('book_db.xlsx')  # import를 위해서 dataori
data = dataori

vectorizer = TfidfVectorizer(min_df = 2000, sublinear_tf = True)
vectorizerfit = vectorizer.fit(data['total'])
vecdf = vectorizer.transform(data['total']).toarray()

word_list = sorted(vectorizerfit.vocabulary_.items()) # 단어사전을 정렬합니다.

# 용이한 시각화를 위하여 데이터프레임 변환
tf_idf_df = pd.DataFrame(vecdf, columns = word_list, index = data.제목)
# 코사인 유사도 계산
cos_sim_df = pd.DataFrame(cosine_similarity(tf_idf_df, tf_idf_df))



def home(request):
    a = User.objects.filter(username = request.user).values('id')
    e_id = a.values('id')[0]['id']
    choo1 = MYCHOOSE.objects.filter(user_id = e_id).values('Action')
    choo2 = MYCHOOSE.objects.filter(user_id = e_id).values('Adventure')
    choo3 = MYCHOOSE.objects.filter(user_id = e_id).values('Animation')
    choo4 = MYCHOOSE.objects.filter(user_id = e_id).values('Comedy')
    choo5 = MYCHOOSE.objects.filter(user_id = e_id).values('Crime')
    choo6 = MYCHOOSE.objects.filter(user_id = e_id).values('Documentary')
    choo7 = MYCHOOSE.objects.filter(user_id = e_id).values('Drama')
    choo8 = MYCHOOSE.objects.filter(user_id = e_id).values('Family')
    choo9 = MYCHOOSE.objects.filter(user_id = e_id).values('Fantasy')
    choo10 = MYCHOOSE.objects.filter(user_id = e_id).values('History')
    choo11 = MYCHOOSE.objects.filter(user_id = e_id).values('Horror')
    choo12 = MYCHOOSE.objects.filter(user_id = e_id).values('Music')
    choo13 = MYCHOOSE.objects.filter(user_id = e_id).values('Mystery')
    choo14 = MYCHOOSE.objects.filter(user_id = e_id).values('Romance')
    choo15 = MYCHOOSE.objects.filter(user_id = e_id).values('ScienceFiction')
    choo16 = MYCHOOSE.objects.filter(user_id = e_id).values('TVMovie')
    choo17 = MYCHOOSE.objects.filter(user_id = e_id).values('Thriller')
    choo18 = MYCHOOSE.objects.filter(user_id = e_id).values('War')
    choo19 = MYCHOOSE.objects.filter(user_id = e_id).values('Western')
    choo = choo1.exists()+choo2.exists()+choo3.exists()+choo4.exists()+choo5.exists()+choo6.exists()+choo7.exists()+choo8.exists()+choo9.exists()+choo10.exists()+choo11.exists()+choo12.exists()+choo13.exists()+choo14.exists()+choo15.exists()+choo16.exists()+choo17.exists()+choo18.exists()+choo19.exists()     
   


    # MYCHOO DATA가 있으면 home, 없으면 choose
    if choo:
        
        page = 1
        list = []
        Key = 'ttbsaspower81040001'


        book_id = MYSELECT.objects.filter(user_id = e_id).values('book_id')
        book_sel_data = pd.DataFrame()
        for l in range(0,len(book_id)):
            book_sel_data = pd.concat([book_sel_data, data[data['id'] == int(book_id[l]['book_id'])]])


        
        # 유저 평점 기반으로 도서 추천
        star_a = MYSTAR.objects.all()
        star_aa=pd.DataFrame(star_a.values())
        # print(star_aa['user_id'])
        
        try : # 
            # 현재 사용자
            star_1 = MYSTAR.objects.filter(user_id=e_id)
            star_11=pd.DataFrame(star_1.values())
            star_111 = star_11['user_id'][0] # 사용자의 id

            # 1
            def matrix_factorization(R, K, step=200, learning_rate=0.01, r_lambda=0.01):
                num_users, num_items = R.shape
                np.random.seed(0)
                P = np.random.normal(scale=1./K, size=(num_users, K))  
                Q = np.random.normal(scale=1./K, size=(num_items, K))  
                non_zeros = [ (i,j,R[i,j]) for i in range(num_users) for j in range(num_items) if R[i,j] > 0 ]
                for step in range(step): 
                    for i, j, r in non_zeros:
                        e_ij = r - np.dot(P[i,:], Q[j,:].T)
                        P[i,:] = P[i,:] + learning_rate*(e_ij * Q[j,:] - r_lambda*P[i,:])
                        Q[j,:] = Q[j,:] + learning_rate*(e_ij * P[i,:] - r_lambda*Q[j,:])     
                return P, Q
            # 2
            star_matrix = star_aa.pivot_table(index='user_id', columns='book_id', values='star')
            P,Q = matrix_factorization(star_matrix.values, K=50, step=200, 
                                    learning_rate=0.01, r_lambda=0.01)
            pred_matrix = np.dot(P, Q.T)
            # 3
            star_pred_matrix = pd.DataFrame(pred_matrix, index=star_matrix.index,
                                            columns=star_matrix.columns)
            # 4
            def get_unseen_book(star_matrix, user_id):
                user_star = star_matrix.loc[user_id]
                already_seen = user_star[user_star >0].index.tolist()
                book_list = star_matrix.columns.tolist()
                unseen_list = set(book_list).difference(set(already_seen))
                return unseen_list

            def recomm_book_by_userId(pred_df, user_id, unseen_list, top_n=5):
                recomm_book = pred_df.loc[user_id, unseen_list].sort_values(ascending=False)[:top_n]
                return recomm_book

            unseen_list = get_unseen_book(star_matrix, star_111) # star_111 : 현재 user_id
            recomm_book = recomm_book_by_userId(star_pred_matrix, star_111, unseen_list, top_n=5)
            recomm_book = pd.DataFrame(recomm_book.values, index=recomm_book.index,
                                        columns=['pred_score'])
            recomm_book = recomm_book.reset_index()

            ii = pd.DataFrame()
            for i in recomm_book['book_id'].values:
                ii = pd.concat([ii, pd.DataFrame(data[data['id'] == int(i)])])
        
            response_data_star = ii.to_dict('records') # 별점 기반 다른 사용자로부터 추천

        except : 
            response_data_star = [] # 별점 기반 다른 사용자로부터 추천
        
        
        response_data2 = book_sel_data.to_dict('records') # 유저 추천

        response_data = data.head(20).to_dict('records')

        response_top10 = data.sort_values('추천수_단위', ascending=False).head(10).to_dict('records')

        response_sf = data[data['keyword'].str.contains('로맨스')].sort_values('추천수_단위', ascending=False).head(20).to_dict('records')
                
        response_fear = data[data['keyword'].str.contains('판타지')].sort_values('추천수_단위', ascending=False).head(20).to_dict('records')
        
        response_new = data.sort_values('조회수_단위').head(20).to_dict('records')

        

        context = {
            'response_data': response_data,
            'response_data2': response_data2,
            'response_top10': response_top10,
            'response_sf': response_sf,
            'response_fear': response_fear,
            'response_new': response_new,
            'response_data_star' : response_data_star
        }
        return render(request, "board/home.html", context)



   
    else:   # 장르 데이터베이스 없을 시 choose로

        apikey = '6b75188cf5cbc494ffe18d4d302e3aaa'

        url = f'https://api.themoviedb.org/3/movie/popular?api_key={apikey}&language=ko-KR&page=1&region=KR'
        genre_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={apikey}&language=ko-KR'
        respon = requests.get(url).json()['results'] # 영화 세부 정보 딕셔너리
        res_gen = requests.get(genre_url).json()['genres'] # 장르 딕셔너리 {숫자:장르}
        
        for item in respon :
            gen_list = []
            for i in range(len(res_gen)):
                gen_list += res_gen[i].values()
            
            gen_ko = []
            for j in range(len(item['genre_ids'])):
                a = gen_list[gen_list.index(item['genre_ids'][j])-1]
                gen_ko.append(a)
           
            item['gen_ko'] = gen_ko # 장르id를 한글장르로 바꾼 키 추가
            
        context = {
            'respon': respon,
        }

        return render(request, 'user/choose.html', context)


def BoardDetailView(request, pk):
    """상세페이지"""
    # 웹에서 받아온 pk(id)값과 책DB의 id값이 같은 책 데이터를 딕셔너리 형태로 받아옴
    detail_data = data[data['id'] == int(pk)].to_dict('records')
    # 책에 키워드가 존재하면 keyword에 리스트 형태로 저장
    if len(eval(data[data['id'] == int(pk)]['keyword'].iloc[0])) > 0:
        keyword = eval(data[data['id'] == int(pk)]['keyword'].iloc[0])
        # print(keyword)


    # 인트로 유사도 검사 뒤
    book_id3 = pk

    intro_sim_sorted_idx = cos_sim_df[int(book_id3)].sort_values(ascending=False)[0:11]
    similar_book = data.loc[intro_sim_sorted_idx.index]

    response_intro = similar_book.to_dict('records')[1:6]


    isbook = False # 책이 있는지 없는지 검사하는 값
    if request.method == "POST":
        id = request.POST['id'] # html form안의 input 태그에서 가져옴 (input태그 id가 id인 경우)
        user_id = User.objects.get(id = id).id # 위와 데이터베이스 같은지 (현재 로그인한 회원과)
        my_book = MYBOOK.objects.filter(user_id = user_id).filter(book_id = pk) # 위의 상황이 true일때 책 아이디 가져옴.

        star = MYSTAR.objects.filter(user_id=id).filter(book_id=pk).values('star')

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

    else:

        context = {
            'detail_data': detail_data, # 책 정보
            'keyword': keyword, # 책 키워드 리스트
            'isbook': isbook,
            'response_intro' : response_intro, # 유사도검사 인트로
            # 'star' : star,
        }
        return render(request, "board/detail.html", context)



def search(request, **kwargs):
    # HttpRequest 객체를 통해 전달받은 검색어를 변수에 저장

    search_word = request.GET.get('searchWord')
    search_type = request.GET.get('searchType')
    sort_type = request.GET.get('sortType')
    sort_type2 = request.GET.get('sortType2')
    genre_word = request.GET.get('genreWord')
    if genre_word:
        search_word = '#'
   
    if search_word in ('', ' ', '\\'):
        response = []
        empty = True
        context = {
            'empty': empty,
            'response': response,
            'searchType': search_type,
            'sortType': sort_type,
            'pr_text': search_word,
        }
        return render(request, "board/search.html", context)

    elif search_type: # 검색기준 및 검색어를 전달받은 경우
        match search_type:
            case 'title':
                if sort_type == 'CustomerRating':
                    response = data[data['제목'].str.contains(search_word)].sort_values('추천수_단위', ascending=False).to_dict('records')
                else:
                    response = data[data['제목'].str.contains(search_word)].sort_values('조회수_단위', ascending=False).to_dict('records')

                # print(len(response))
                page = request.GET.get('page', '1')  # 페이지
                paginator = Paginator(response, 10)  # 페이지당 10개씩 보여주기
                page_obj = paginator.get_page(page)


                context = {
                    'total': response,
                    'response': page_obj,
                    'searchType': search_type,
                    'sortType': sort_type,
                    'pr_text': search_word,
                }

                return render(request, "board/search.html", context)

            case 'author':
                if sort_type == 'CustomerRating':
                    response = data[data['작가'].str.contains(search_word)].sort_values('추천수_단위', ascending=False).to_dict('records')
                else:
                    response = data[data['작가'].str.contains(search_word)].sort_values('조회수_단위', ascending=False).to_dict('records')

                page = request.GET.get('page', '1')  # 페이지
                paginator = Paginator(response, 10)  # 페이지당 10개씩 보여주기
                page_obj = paginator.get_page(page)
                # print(response)
                context = {
                    'total': response,
                    'response': page_obj,
                    'searchType': search_type,
                    'sortType': sort_type,
                    'pr_text': search_word,
                }

                return render(request, "board/search.html", context)

            case 'keyword':
                # 키워드 검색 기능
                if sort_type == 'CustomerRating':
                    response = data[data['keyword'].str.contains(search_word)].sort_values('추천수_단위', ascending=False).to_dict('records')
                else:
                    response = data[data['keyword'].str.contains(search_word)].sort_values('조회수_단위', ascending=False).to_dict('records')

                page = request.GET.get('page', '1')  # 페이지
                paginator = Paginator(response, 10)  # 페이지당 10개씩 보여주기
                page_obj = paginator.get_page(page)
                # print(response)
                context = {
                    'total': response,
                    'response': page_obj,
                    'searchType': search_type,
                    'sortType': sort_type,
                    'pr_text': search_word,
                }

                return render(request, "board/search.html", context)
            
            case 'genre':
                # 사이드바 장르
                if sort_type2 == 'end':
                    if sort_type == 'CustomerRating':
                        response = data[np.logical_and(data['장르'] == genre_word, data['tag'] == '완결')].sort_values('추천수_단위', ascending=False).to_dict('records')
                    else:
                        response = data[np.logical_and(data['장르'] == genre_word, data['tag'] == '완결')].sort_values('조회수_단위', ascending=False).to_dict('records')
                elif sort_type2 == 'new':
                    if sort_type == 'CustomerRating':
                        response = data[np.logical_and(data['장르'] == genre_word, data['tag'] == '최신')].sort_values('추천수_단위', ascending=False).to_dict('records')
                    else:
                        response = data[np.logical_and(data['장르'] == genre_word, data['tag'] == '최신')].sort_values('조회수_단위', ascending=False).to_dict('records')
                else:
                    if genre_word == '로맨스':
                        if sort_type == 'CustomerRating':
                            response = data[np.logical_or(data['장르'] == '판타지', data['장르'] == '로판')].sort_values('추천수_단위', ascending=False).to_dict('records')
                        else:
                            response = data[np.logical_or(data['장르'] == '판타지', data['장르'] == '로판')].sort_values('조회수_단위', ascending=False).to_dict('records')
                    elif genre_word == 'BL':
                        if sort_type == 'CustomerRating':
                            response = data[data['장르'] == 'BL'].sort_values('추천수_단위', ascending=False).to_dict('records')
                        else:
                            response = data[data['장르'] == 'BL'].sort_values('조회수_단위', ascending=False).to_dict('records')
                    else:
                        if sort_type == 'CustomerRating':
                            response = data[np.logical_or(data['장르'] == '판타지', data['장르'] == '무협')].sort_values('추천수_단위', ascending=False).to_dict('records')
                        else:
                            response = data[np.logical_or(data['장르'] == '판타지', data['장르'] == '무협')].sort_values('조회수_단위', ascending=False).to_dict('records')

                pr_text = ''
                page = request.GET.get('page', '1')  # 페이지
                paginator = Paginator(response, 10)  # 페이지당 10개씩 보여주기
                page_obj = paginator.get_page(page)
                # print(response)
                context = {
                    'total': response,
                    'response': page_obj,
                    'searchType': search_type,
                    'sortType': sort_type,
                    'sortType2': sort_type2,
                    'pr_text': pr_text,
                    'genre_text': genre_word,
                }

                return render(request, "board/search.html", context)

                        
    else:
        return render(request, "board/search.html")

