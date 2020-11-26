from django.shortcuts import render
from .secrets import apiKey
from .models import Place
import requests


# def index(request):
#     return render(request, "index.html")

def get_random():
    return Place.objects.order_by("?").first()


def index(request):
    return render(request, 'index.html')


def random(request):
    keynum = apiKey
    api_key_decode = requests.utils.unquote(keynum)
    # place = Place.objects.get(name="yeosu")
    place = get_random()
    # print(type(place))
    pname = place.name
    areaCode = place.areaCode
    sigunguCode = place.sigunguCode

    # print("현재 장소 :", pname, areaCode, sigunguCode)
    if sigunguCode == 0:
        sigunguCode = ""
    payload = {'ServiceKey': api_key_decode, 'numOfRows': 12, 'pageNo': 1,
               'MobileOS': 'ETC', 'MobileApp': 'AppTest', 'areaCode': areaCode, 'sigunguCode': sigunguCode, 'cat1': 'A02', 'listYN': 'Y', '_type': 'json', 'arrange': 'P', 'overviewYN': 'Y'}

    r = requests.get(
        'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList', params=payload)

    data = r.json()
    # print(data)
    items = data['response']['body']['items']['item']
    print(items[1])
    for item in items:
        print(item['title'])
        print(item)

    return render(request, 'random.html', {'items': items, 'place': place})
