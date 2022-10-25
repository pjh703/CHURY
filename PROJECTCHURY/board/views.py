from django.shortcuts import render
import requests

# Create your views here.

def home(request):

    page = 1
    list = []
    Key = 'ttbsaspower81040001'
    categor = '170370'

    # open API 주소를 이용합니다. json으로 받아옵니다.
    apiurl =f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={Key}&QueryType=Bestseller&MaxResults=10&start=1&SearchTarget=eBook&Cover=Big&CategoryId={categor}&output=js&Version=20131101"
        # requests를 이용하여 json을 불러옵니다.
    response = requests.get(apiurl).json()
    # print(response)

    # if response['item'] != []:
    #     for i in range (0, 10):
    #         print("제목: ", response['item'][i]['title'])
    #         print("작가: ", response['item'][i]['author'])
    #         print("표지: ", response['item'][i]['cover'])
    #         print("장르: ", response['item'][i]['categoryName'])
    #         if response['item'][i]['description']:
    #             print("요약: ", response['item'][i]['description'])
    #         print("평점: ", response['item'][i]['customerReviewRank'])
    #         print("상세링크: ", response['item'][i]['link'])
    #         print("=========================================")
    # else:
    #     print("검색 결과가 없습니다.")
    context = {
        'response': response['item'],
    }

    return render(request, "board/home.html", context)