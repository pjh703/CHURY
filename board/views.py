import requests

from lib2to3.pgen2.token import DOUBLESTAREQUAL

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from django.views.generic import DetailView
from user.models import User
from mypage.models import MYBOOK, MYCHOOSE
from xlrd import open_workbook
from django.core.paginator import Paginator  

import numpy as np
import pandas as pd
import math


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
   

    # MYCHOO DATA??? ????????? home, ????????? choose
    if choo:
        
        page = 1
        list = []
        Key = 'ttbsaspower81040001'

        response_data = data.head(20).to_dict('records') # ?????? ??????

        response_top10 = data.sort_values('?????????_??????', ascending=False).head(10).to_dict('records')

        response_sf = data[data['keyword'].str.contains('sf')].sort_values('?????????_??????', ascending=False).head(20).to_dict('records')
                
        response_fear = data[data['keyword'].str.contains('??????')].sort_values('?????????_??????', ascending=False).head(20).to_dict('records')
        
        response_new = data.sort_values('?????????_??????').head(20).to_dict('records')

        context = {
            'response_data': response_data,
            'response_top10': response_top10,
            'response_sf': response_sf,
            'response_fear': response_fear,
            'response_new': response_new
        }

        return render(request, "board/home.html", context)
    

    # ?????? ?????????????????? ?????? ??? choose???
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
    """???????????????"""
    # ????????? ????????? pk(id)?????? ???DB??? id?????? ?????? ??? ???????????? ???????????? ????????? ?????????
    detail_data = data[data['id'] == int(pk)].to_dict('records')
    # ?????? ???????????? ???????????? keyword??? ????????? ????????? ??????
    if len(eval(data[data['id'] == int(pk)]['keyword'].iloc[0])) > 0:
        keyword = eval(data[data['id'] == int(pk)]['keyword'].iloc[0])
        # print(keyword)

    isbook = False # ?????? ????????? ????????? ???????????? ???
    if request.method == "POST":
        id = request.POST['id']
        user_id = User.objects.get(id = id).id
        my_book = MYBOOK.objects.filter(user_id = user_id).filter(book_id = pk)

        # print(my_book)
        # print(len(my_book))


        if len(my_book) > 0:
            isbook = True # ?????? ???????????? ?????? ??????

        context = {
            'detail_data': detail_data, # ??? ??????
            'keyword': keyword, # ??? ????????? ?????????
            'isbook': isbook # ?????? ???????????? true???
        }
        return render(request, "board/detail.html", context)

    else:
        # print("get")
        # print(response)

        context = {
            'detail_data': detail_data, # ??? ??????
            'keyword': keyword, # ??? ????????? ?????????
            'isbook': isbook,
        }
        return render(request, "board/detail.html", context)



def search(request, **kwargs):
    # HttpRequest ????????? ?????? ???????????? ???????????? ????????? ??????

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

    elif search_type: # ???????????? ??? ???????????? ???????????? ??????
        match search_type:
            case 'title':
                if sort_type == 'CustomerRating':
                    response = data[data['??????'].str.contains(search_word)].sort_values('?????????_??????', ascending=False).to_dict('records')
                else:
                    response = data[data['??????'].str.contains(search_word)].sort_values('?????????_??????', ascending=False).to_dict('records')

                # print(len(response))
                page = request.GET.get('page', '1')  # ?????????
                paginator = Paginator(response, 10)  # ???????????? 10?????? ????????????
                page_obj = paginator.get_page(page)
                # pagination = {}
                # for i in range(math.ceil((len(response)/10))):
                #     print(i)
                #     if i+1 == (math.ceil((len(response)/10))):
                #         pagination[i] = response[-(len(response)%10):]
                #     else:
                #         pagination[i] = response[10*i:10*(i+1)]
                
                # print(pagination[page-1])
                # print(page_dic)
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
                    response = data[data['??????'].str.contains(search_word)].sort_values('?????????_??????', ascending=False).to_dict('records')
                else:
                    response = data[data['??????'].str.contains(search_word)].sort_values('?????????_??????', ascending=False).to_dict('records')

                page = request.GET.get('page', '1')  # ?????????
                paginator = Paginator(response, 10)  # ???????????? 10?????? ????????????
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
                # ????????? ?????? ??????
                if sort_type == 'CustomerRating':
                    response = data[data['keyword'].str.contains(search_word)].sort_values('?????????_??????', ascending=False).to_dict('records')
                else:
                    response = data[data['keyword'].str.contains(search_word)].sort_values('?????????_??????', ascending=False).to_dict('records')

                page = request.GET.get('page', '1')  # ?????????
                paginator = Paginator(response, 10)  # ???????????? 10?????? ????????????
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
                # ???????????? ??????
                if sort_type2 == 'end':
                    if sort_type == 'CustomerRating':
                        response = data[np.logical_and(data['??????'] == genre_word, data['tag'] == '??????')].sort_values('?????????_??????', ascending=False).to_dict('records')
                    else:
                        response = data[np.logical_and(data['??????'] == genre_word, data['tag'] == '??????')].sort_values('?????????_??????', ascending=False).to_dict('records')
                elif sort_type2 == 'new':
                    if sort_type == 'CustomerRating':
                        response = data[np.logical_and(data['??????'] == genre_word, data['tag'] == '??????')].sort_values('?????????_??????', ascending=False).to_dict('records')
                    else:
                        response = data[np.logical_and(data['??????'] == genre_word, data['tag'] == '??????')].sort_values('?????????_??????', ascending=False).to_dict('records')
                else:
                    if genre_word == '?????????':
                        if sort_type == 'CustomerRating':
                            response = data[np.logical_or(data['??????'] == '?????????', data['??????'] == '??????')].sort_values('?????????_??????', ascending=False).to_dict('records')
                        else:
                            response = data[np.logical_or(data['??????'] == '?????????', data['??????'] == '??????')].sort_values('?????????_??????', ascending=False).to_dict('records')
                    elif genre_word == 'BL':
                        if sort_type == 'CustomerRating':
                            response = data[data['??????'] == 'BL'].sort_values('?????????_??????', ascending=False).to_dict('records')
                        else:
                            response = data[data['??????'] == 'BL'].sort_values('?????????_??????', ascending=False).to_dict('records')
                    else:
                        if sort_type == 'CustomerRating':
                            response = data[np.logical_or(data['??????'] == '?????????', data['??????'] == '??????')].sort_values('?????????_??????', ascending=False).to_dict('records')
                        else:
                            response = data[np.logical_or(data['??????'] == '?????????', data['??????'] == '??????')].sort_values('?????????_??????', ascending=False).to_dict('records')

                pr_text = ''
                page = request.GET.get('page', '1')  # ?????????
                paginator = Paginator(response, 10)  # ???????????? 10?????? ????????????
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