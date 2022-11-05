import requests

from lib2to3.pgen2.token import DOUBLESTAREQUAL

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from django.views.generic import DetailView
from xlrd import open_workbook



# Create your views here.

def home(request):

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



def BoardDetailView(request, pk):
    page = 1
    list = []
    Key = 'ttbsaspower81040001'
    categor = '170370'

    apiurl =f"http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey={Key}&itemIdType=ISBN&ItemId={pk}&Cover=Big&output=js&Version=20131101&OptResult=ebookList,usedList,reviewList"
    response = requests.get(apiurl).json()
    
    # print(response)
    context = {
        'response': response['item'],
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
                    page = 1
                    list = []
                    Key = 'ttbsaspower81040001'
                    
                    if sort_type == 'SalesPoint':
                        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={Key}&Query={search_word}&QueryType=title&MaxResults=10&start=1&SearchTarget=eBook&Sort=SalesPoint&Cover=Big&output=js&Version=20131101"
                    elif sort_type == 'CustomerRating':
                        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={Key}&Query={search_word}&QueryType=title&MaxResults=10&start=1&SearchTarget=eBook&Sort=CustomerRating&Cover=Big&output=js&Version=20131101"
                    else:
                        apiurl =f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={Key}&Query={search_word}&QueryType=title&MaxResults=10&start=1&SearchTarget=eBook&Sort=PublishTime&Cover=Big&output=js&Version=20131101"
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

                    page = 1
                    list = []
                    Key = 'ttbsaspower81040001'
                    COUNT = 0
                    for row in range(1, sheet.nrows):
                        if sheet.cell_value(row, column_index) == '전자책':
                            if search_word == '':
                                response = {'status': 'empty'}
                            elif search_word in sheet.cell_value(row, column_index + 1):
                                categor = (int)(sheet.cell_value(row, column_index - 2))
                                if query_type == 'ItemNewAll':
                                    apiurl =f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={Key}&QueryType=ItemNewAll&MaxResults=10&start=1&SearchTarget=eBook&Cover=Big&CategoryId={categor}&output=js&Version=20131101"
                                else:
                                    apiurl =f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={Key}&QueryType=Bestseller&MaxResults=10&start=1&SearchTarget=eBook&Cover=Big&CategoryId={categor}&output=js&Version=20131101"
                                # requests를 이용하여 json을 불러옵니다.
                                response = requests.get(apiurl).json()
                                break
                            else:
                                response = {'status': 'empty'}
                    
                    context = {
                        'response': response,
                        'searchType': search_type,
                        'queryType': query_type,
                        'pr_text': search_word,
                    }

                    return render(request, "board/search.html", context)

                        
    else:
        return render(request, "board/search.html")