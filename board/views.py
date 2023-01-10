import requests

from lib2to3.pgen2.token import DOUBLESTAREQUAL

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from django.views.generic import DetailView
from user.models import User
from mypage.models import MYBOOK, MYCHOOSE
from xlrd import open_workbook

import numpy as np
import pandas as pd


data = pd.read_excel('book_db.xlsx')


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

        response_data = data.head(20).to_dict('records') # 유저 추천

        response_top10 = data.sort_values('추천수_단위', ascending=False).head(10).to_dict('records')

        response_sf = data[data['keyword'].str.contains('sf')].sort_values('추천수_단위', ascending=False).head(20).to_dict('records')
                
        response_fear = data[data['keyword'].str.contains('공포')].sort_values('추천수_단위', ascending=False).head(20).to_dict('records')
        
        response_new = data.sort_values('조회수_단위').head(20).to_dict('records')

        context = {
            'response_data': response_data,
            'response_top10': response_top10,
            'response_sf': response_sf,
            'response_fear': response_fear,
            'response_new': response_new
        }

        return render(request, "board/home.html", context)
    

    # 장르 데이터베이스 없을 시 choose로
    else:

        apikey = '6b75188cf5cbc494ffe18d4d302e3aaa'

        url = f'https://api.themoviedb.org/3/movie/popular?api_key={apikey}&language=ko-KR&page=1&region=KR'
        genre_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={apikey}&language=ko-KR'
        respon = requests.get(url).json()['results']
        res_gen = requests.get(genre_url).json()['genres']
        
        for item in respon :
            gen_list = []
            for i in range(len(res_gen)):
                gen_list += res_gen[i].values()
            
            gen_ko = []
            for j in range(len(item['genre_ids'])):
                a = gen_list[gen_list.index(item['genre_ids'][j])-1]
                gen_ko.append(a)
           
            item['gen_ko'] = gen_ko
            
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

    isbook = False # 책이 있는지 없는지 검사하는 값
    if request.method == "POST":
        id = request.POST['id']
        user_id = User.objects.get(id = id).id
        my_book = MYBOOK.objects.filter(user_id = user_id).filter(book_id = pk)

        # print(my_book)
        # print(len(my_book))


        if len(my_book) > 0:
            isbook = True # 책이 저장되어 있는 경우

        context = {
            'detail_data': detail_data, # 책 정보
            'keyword': keyword, # 책 키워드 리스트
            'isbook': isbook # 책이 있나없나 true값
        }
        return render(request, "board/detail.html", context)

    else:
        # print("get")
        # print(response)

        context = {
            'detail_data': detail_data, # 책 정보
            'keyword': keyword, # 책 키워드 리스트
            'isbook': isbook,
        }
        return render(request, "board/detail.html", context)



def search(request, **kwargs):
    # HttpRequest 객체를 통해 전달받은 검색어를 변수에 저장

    search_word = request.GET.get('searchWord')
    search_type = request.GET.get('searchType')
    sort_type = request.GET.get('sortType')

    if search_word in ('', ' '):
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

    elif search_word and search_type: # 검색기준 및 검색어를 전달받은 경우
        match search_type:
            case 'title':
                if sort_type == 'CustomerRating':
                    response = data[data['제목'].str.contains(search_word)].sort_values('추천수_단위', ascending=False).to_dict('records')
                else:
                    response = data[data['제목'].str.contains(search_word)].sort_values('조회수_단위', ascending=False).to_dict('records')

                # print(response)
                context = {
                    'response': response,
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

                # print(response)
                context = {
                    'response': response,
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

                # print(response)
                context = {
                    'response': response,
                    'searchType': search_type,
                    'sortType': sort_type,
                    'pr_text': search_word,
                }

                return render(request, "board/search.html", context)
            
            case 'genre':
                # 사이드바 장르
                if sort_type == 'end':
                    response = data[np.logical_and(data['장르'] == search_word, data['tag'] == '완결')].sort_values('추천수_단위', ascending=False).to_dict('records')
                elif sort_type == 'new':
                    response = data[np.logical_and(data['장르'] == search_word, data['tag'] == '최신')].sort_values('추천수_단위', ascending=False).to_dict('records')
                else:
                    if search_word == '로맨스':
                        response = data[np.logical_or(data['장르'] == '판타지', data['장르'] == '로판')].sort_values('추천수_단위', ascending=False).to_dict('records')
                    elif search_word == 'BL':
                        response = data[data['장르'] == 'BL'].sort_values('추천수_단위', ascending=False).to_dict('records')
                    else:
                        response = data[np.logical_or(data['장르'] == '판타지', data['장르'] == '무협')].sort_values('추천수_단위', ascending=False).to_dict('records')

                pr_text = ''
                # print(response)
                context = {
                    'response': response,
                    'searchType': search_type,
                    'sortType': sort_type,
                    'pr_text': pr_text,
                    'genre_text': search_word,
                }

                return render(request, "board/search.html", context)

                        
    else:
        return render(request, "board/search.html")