import requests

from lib2to3.pgen2.token import DOUBLESTAREQUAL

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from django.views.generic import DetailView
from user.models import User
from mypage.models import MYBOOK, MYCHOOSE
from xlrd import open_workbook



# Create your views here.

def home(request):
    a = User.objects.filter(username = request.user).values('id')
    e_id = a.values('id')[0]['id']
    choo1 = MYCHOOSE.objects.filter(email_id = e_id).values('Action')
    choo2 = MYCHOOSE.objects.filter(email_id = e_id).values('Adventure')
    choo3 = MYCHOOSE.objects.filter(email_id = e_id).values('Animation')
    choo4 = MYCHOOSE.objects.filter(email_id = e_id).values('Comedy')
    choo5 = MYCHOOSE.objects.filter(email_id = e_id).values('Crime')
    choo6 = MYCHOOSE.objects.filter(email_id = e_id).values('Documentary')
    choo7 = MYCHOOSE.objects.filter(email_id = e_id).values('Drama')
    choo8 = MYCHOOSE.objects.filter(email_id = e_id).values('Family')
    choo9 = MYCHOOSE.objects.filter(email_id = e_id).values('Fantasy')
    choo10 = MYCHOOSE.objects.filter(email_id = e_id).values('History')
    choo11 = MYCHOOSE.objects.filter(email_id = e_id).values('Horror')
    choo12 = MYCHOOSE.objects.filter(email_id = e_id).values('Music')
    choo13 = MYCHOOSE.objects.filter(email_id = e_id).values('Mystery')
    choo14 = MYCHOOSE.objects.filter(email_id = e_id).values('Romance')
    choo15 = MYCHOOSE.objects.filter(email_id = e_id).values('ScienceFiction')
    choo16 = MYCHOOSE.objects.filter(email_id = e_id).values('TVMovie')
    choo17 = MYCHOOSE.objects.filter(email_id = e_id).values('Thriller')
    choo18 = MYCHOOSE.objects.filter(email_id = e_id).values('War')
    choo19 = MYCHOOSE.objects.filter(email_id = e_id).values('Western')
    choo = choo1.exists()+choo2.exists()+choo3.exists()+choo4.exists()+choo5.exists()+choo6.exists()+choo7.exists()+choo8.exists()+choo9.exists()+choo10.exists()+choo11.exists()+choo12.exists()+choo13.exists()+choo14.exists()+choo15.exists()+choo16.exists()+choo17.exists()+choo18.exists()+choo19.exists()     
   

    # MYCHOO DATA가 있으면 home, 없으면 choose
    if choo:
        
        page = 1
        list = []
        Key = 'ttbsaspower81040001'

        categor = '170370'
        # open API 주소를 이용합니다. json으로 받아옵니다.
        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={Key}&QueryType=Bestseller&MaxResults=20&start=1&SearchTarget=eBook&Cover=Big&CategoryId={categor}&output=js&Version=20131101"
            # requests를 이용하여 json을 불러옵니다.
        response = requests.get(apiurl).json()
        # print(response)

        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={Key}&QueryType=Bestseller&MaxResults=10&start=1&SearchTarget=eBook&Cover=Big&output=js&Version=20131101"
        response_top10 = requests.get(apiurl).json()


        wb = open_workbook('board/aladin_Category.xls')
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        column_index = 2
        column = sheet.cell_value(0, column_index)

        categor_sf = '40112'
        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={Key}&QueryType=Bestseller&MaxResults=20&start=1&SearchTarget=eBook&Cover=Big&CategoryId={categor_sf}&output=js&Version=20131101"
        response_sf = requests.get(apiurl).json()
                
        categor_fear = '56552'
        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={Key}&QueryType=Bestseller&MaxResults=10&start=1&SearchTarget=eBook&Cover=Big&CategoryId={categor_fear}&output=js&Version=20131101"
        response_fear = requests.get(apiurl).json()
        
        
        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={Key}&QueryType=ItemNewSpecial&MaxResults=20&start=1&SearchTarget=eBook&Cover=Big&output=js&Version=20131101"
        response_new = requests.get(apiurl).json()
        
        context = {
            'response': response,
            'response_top10': response_top10,
            'response_sf': response_sf,
            'response_fear': response_fear,
            'response_new': response_new,
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
    page = 1
    list = []
    Key = 'ttbsaspower81040001'

    apiurl =f"http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey={Key}&itemIdType=ISBN13&ItemId={pk}&Cover=Big&output=js&Version=20131101&OptResult=ebookList,usedList,reviewList"
    response = requests.get(apiurl).json()

    isbook = True
    # 책이 있나없나 검사
    if request.method == "POST":
        email = request.POST['email']
        email_id = User.objects.get(email = email).id
        mydic = MYBOOK.objects.filter(email_id = email_id).values('mydic').filter(mydic = pk)
        mydic1 = MYBOOK.objects.filter(email_id = email_id).filter(mydic = pk)
        myread = MYBOOK.objects.filter(email_id = email_id).values('mydic').filter(mydic = pk).values('myread')[0].get('myread')

        # print(mydic1)
        # print("post")
        print(myread)


        if len(mydic) > 0:
            isbook = False # 책이 저장되어 있는 경우

        # print(response)
        context = {
            'response': response, # 책정보 보내줌
            'isbook': isbook, # 책이 있나없나 true값
            'myread': myread
        }
        return render(request, "board/detail.html", context)

    else:
        # print("get")
        # print(response)

        context = {
            'response': response,
            'isbook': isbook,
        }
        return render(request, "board/detail.html", context)



def search(request, **kwargs):
    # HttpRequest 객체를 통해 전달받은 검색어를 변수에 저장

    search_word = request.GET.get('searchWord')
    search_type = request.GET.get('searchType')
    sort_type = request.GET.get('sortType')
    query_type = request.GET.get('queryType')
    
    if search_type and search_type: # 검색기준 및 검색어를 전달받은 경우
            match search_type:
                case 'title':
                    page = request.GET.get('page', 1)
                    list = []
                    Key = 'ttbsaspower81040001'
                    
                    if sort_type == 'SalesPoint':
                        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={Key}&Query={search_word}&QueryType=title&MaxResults=10&start={page}&SearchTarget=eBook&Sort=SalesPoint&Cover=Big&output=js&Version=20131101"
                    elif sort_type == 'CustomerRating':
                        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={Key}&Query={search_word}&QueryType=title&MaxResults=10&start={page}&SearchTarget=eBook&Sort=CustomerRating&Cover=Big&output=js&Version=20131101"
                    else:
                        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={Key}&Query={search_word}&QueryType=title&MaxResults=10&start={page}&SearchTarget=eBook&Sort=PublishTime&Cover=Big&output=js&Version=20131101"
                    response = requests.get(apiurl).json()

                    # print(response)
                    context = {
                        'response': response,
                        'searchType': search_type,
                        'sortType': sort_type,
                        'pr_text': search_word,
                    }

                    return render(request, "board/search.html", context)

                case 'author':
                    page = request.GET.get('page', 1)
                    list = []
                    Key = 'ttbsaspower81040001'
                    
                    if sort_type == 'SalesPoint':
                        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={Key}&Query={search_word}&QueryType=Author&MaxResults=10&start={page}&SearchTarget=eBook&Sort=SalesPoint&Cover=Big&output=js&Version=20131101"
                    elif sort_type == 'CustomerRating':
                        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={Key}&Query={search_word}&QueryType=Author&MaxResults=10&start={page}&SearchTarget=eBook&Sort=CustomerRating&Cover=Big&output=js&Version=20131101"
                    else:
                        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={Key}&Query={search_word}&QueryType=Author&MaxResults=10&start={page}&SearchTarget=eBook&Sort=PublishTime&Cover=Big&output=js&Version=20131101"
                    response = requests.get(apiurl).json()

                    # print(response)
                    context = {
                        'response': response,
                        'searchType': search_type,
                        'sortType': sort_type,
                        'pr_text': search_word,
                    }

                    return render(request, "board/search.html", context)

                case 'category':
                    # 카테고리 검색 기능
                    wb = open_workbook('board/aladin_Category.xls')
                    sheet = wb.sheet_by_index(0)
                    sheet.cell_value(0, 0)
                    column_index = 2
                    column = sheet.cell_value(0, column_index)

                    page = request.GET.get('page', 1)
                    response = {}
                    response_list = []
                    total_result = 0
                    Key = 'ttbsaspower81040001'
                    COUNT = 0
                    for row in range(1, sheet.nrows):
                        if sheet.cell_value(row, column_index) == '전자책':
                            if search_word == '':
                                response = {'status': 'empty'}
                            elif (search_word in (str)(sheet.cell_value(row, column_index - 1)))|(search_word in (str)(sheet.cell_value(row, column_index + 1))):
                                categor = (int)(sheet.cell_value(row, column_index - 2))
                                if query_type == 'ItemNewAll':
                                    apiurl =f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={Key}&QueryType=ItemNewAll&MaxResults=10&start={page}&SearchTarget=eBook&Cover=Big&CategoryId={categor}&output=js&Version=20131101"
                                else:
                                    apiurl =f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={Key}&QueryType=Bestseller&MaxResults=10&start={page}&SearchTarget=eBook&Cover=Big&CategoryId={categor}&output=js&Version=20131101"
                                # requests를 이용하여 json을 불러옵니다.
                                response_url = requests.get(apiurl).json()
                                response_list.append(response_url['item'])
                                total_result += response_url['totalResults']
                                response['item'] = sum(response_list, [])

                    context = {
                        'response': response,
                        'searchType': search_type,
                        'queryType': query_type,
                        'pr_text': search_word,
                        'total_result' : total_result,
                    }

                    return render(request, "board/search.html", context)

                        
    else:
        return render(request, "board/search.html")