# import requests
# from pprint import pprint

# def uzum():

#     headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
#     request = requests.get("https://uzum.uz/uz/search?query=asus&needsCorrection=1", headers=headers)
#     pprint(request.content)
    
# uzum()

import requests  # veya "import httpx" kullanarak httpx'i kullanabilirsiniz

# API'nin URL'sini ve arama parametrelerini ayarlayın
api_url = 'https://graphql.uzum.uz/'
search_query = 'asus vivobook'  # Arama sorgusu

# İstek başlıklarını ayarlayın (isteğe bağlı)
headers = {
    'Authorization': 'Bearer eyJraWQiOiIwcE9oTDBBVXlWSXF1V0w1U29NZTdzcVNhS2FqYzYzV1N5THZYb0ZhWXRNIiwiYWxnIjoiRWREU0EiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJVenVtIElEIiwiaWF0IjoxNjk1NTcwMjAzLCJzdWIiOiI4NGU1MTljNS04YTFhLTQ5OTgtOTNkMC01MzFkYjM1ZDk1MTYiLCJhdWQiOlsidXp1bV9hcHBzIiwibWFya2V0L3dlYiJdLCJldmVudHMiOnsib3RwX3Bhc3NlZCI6MTY5NDUyMTMzOX0sImN1c3RvbWVyX2lkIjoiNjAyM2I3N2ItYjA2ZS00MzQyLTg2NjgtZDhlMmY0ZTZjNjAzIiwicGhvbmVfbnVtYmVyIjoiOTk4OTkxMjcxNDA1IiwiZXhwIjoxNjk1NTcyMTIzfQ.LqX02bdL-2aDpmWWldzwK13HJhNnVlBfl98i0KYKbacIMmQcmrZwyCVkG36Eu8hFp5FAJv98Bb10n6swZxlJCw',  # API anahtarınızı buraya ekleyin (eğer gerekiyorsa)
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',  # İsteği hangi kullanıcı ajanıyla gönderdiğinizi belirleyin (isteğe bağlı)
}

# İstek parametrelerini veya gövdesini ayarlayın (API belgesine göre)
params = {
    "queryText": "asus" # İhtiyaç duyulan diğer parametreleri ekleyin (isteğe bağlı)
}

# HTTP GET veya POST isteği gönderme (API belgesine göre)
try:
    response = requests.get(api_url, params=params, headers=headers)  # veya "httpx.get" kullanarak httpx'i kullanabilirsiniz
    response.raise_for_status()  # İstek başarısız olursa bir hata fırlatır
except requests.exceptions.RequestException as e:
    print(f'Hata oluştu: {e}')
    response = None

if response:
    data = response.json()  # Yanıtı JSON formatında çözümleyin
    print(data)