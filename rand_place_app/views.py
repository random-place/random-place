from django.shortcuts import render
from .secrets import apiKey
from .models import Place
import requests


def get_random():
    return Place.objects.order_by("?").first()


def get_filter(lst):
    lst = list(map(int, lst))
    return Place.objects.filter(areaCode__in=lst).order_by("?").first()


def index(request):
    return render(request, 'index.html')


def random(request):

    keynum = apiKey
    api_key_decode = requests.utils.unquote(keynum)
    if request.method == 'POST':
        data = request.POST.getlist('area[]')
        print("필터 작동! data = ", data)
        place = get_filter(data)
        if data == []:
            place = get_random()
            print("필터 결과 걍 랜덤")
    else:
        place = get_random()
    print("최종 여행지 : ", place)
    pname = place.name
    areaCode = place.areaCode
    sigunguCode = place.sigunguCode

    if sigunguCode == 0:
        sigunguCode = ""
    contentIdList = [12, 14, 15, 28]
    items = []
    # contentTypeId : 12 (관광) , 14( 문화) , 15 (공연,축제), 28 (레포츠)
    for i, contentId in enumerate(contentIdList):
        payload = {'ServiceKey': api_key_decode, 'numOfRows': 9, 'pageNo': 1, 'contentTypeId': contentId,
                   'MobileOS': 'ETC', 'MobileApp': 'AppTest', 'areaCode': areaCode, 'sigunguCode': sigunguCode, 'listYN': 'Y', '_type': 'json', 'arrange': 'P', 'overviewYN': 'Y'}
        r = requests.get(
            'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList', params=payload)
        data = r.json()
        items.append(data['response']['body']['items']['item'])

    # payload = {'ServiceKey': api_key_decode, 'numOfRows': 10, 'pageNo': 1, 'contentTypeId': 28,
    #            'MobileOS': 'ETC', 'MobileApp': 'AppTest', 'areaCode': areaCode, 'sigunguCode': sigunguCode, 'listYN': 'Y', '_type': 'json', 'arrange': 'P', 'overviewYN': 'Y'}

    # data = r.json()
    # items = data['response']['body']['items']['item']
    # print(items[1])
    # for item in items:
    #     print(item['title'])
    #     print(item)

    return render(request, 'random.html', {'item1': items[0], 'item2': items[1], 'item3': items[2], 'item4': items[3], 'place': place})
