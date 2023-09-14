from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from urllib.parse import quote
from data.data import zoodmall_api_link, sello_api_link, olcha_api_link, texnomart_api_link

def zoodmall(encoded_query, zoodmall_api_link):
    
    url = f"{zoodmall_api_link}{encoded_query}&page=1&sort=1"
    headers = {
        "x-lang": "uz",
        "x-marketcode": "UZ" 
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        
    
        data = response.json()
        products = data['marketList'][0:5]
        API = []
        
        if products:
        
            for product in products:
                API.append(
                    {
                        'name': product['name'],
                        'price': product['totalLocalPrice'],
                        'link': f"https://www.zoodmall.uz/product/{product['productId']}/",
                        'image_link': product['imgUrl']
                    }
                )
            
            def get_price(API):
                price = API.get('price', '0')
                return float(price)
            
            API.sort(key=get_price, reverse=False)
            return API
        else:
            return (f"""Zoodmallda mahsulot topilmadi
                        Status code: {status.HTTP_404_NOT_FOUND}""",  )    
    else:
        print("İstek başarısız oldu. Durum kodu:", response.status_code)
       
def sello(encoded_query, sello_api_link):
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Fingerprint": "10b4ad6ce60f51511b502f34c14f8966",
        "Language": "uz" 
    }
    response = requests.get(f"{sello_api_link}{encoded_query}&page=1&perPage=30", headers=headers)
    
    
    if response.status_code == 200:
        
    
        data = response.json()

        products = data['hits'][0:5]
        API = []
        
        if products:
            for product in products:
                
                if product['discounted_price']:
                    price = product['discounted_price']
                else:
                    price = product['price']
                API.append(
                    {
                        'name': product['name'],
                        'price': price,
                        'link': f"https://sello.uz/uz/product/{product['slug']}/",
                        'image_link': f"https://static.sello.uz/unsafe/x500/https://static.sello.uz{product['imageURL']}"
                    }
                )
            
            def get_price(API):
                price = API.get('price', '0')
                return float(price)
            
            API.sort(key=get_price, reverse=False)
            return API
        else:
            return ("Selloda mahsulot topilmadi,", status.HTTP_404_NOT_FOUND )
    else:
        return ("Status code:", response.status_code)
        
def olcha(encoded_query, olcha_api_link):
    
    headers = {
        "Accept-Language": "oz"
    }
    response = requests.get(f"{olcha_api_link}{encoded_query}", headers=headers)
    
    if response.status_code == 200:    
        data = response.json()
        products = data['data']['products'][0:5]
        API = []
        
        if products:
            for product in products:
                
                if product['discount_price']:
                    price = product['discount_price']
                else:
                    price = product['total_price']
                API.append(
                    {
                        'name': product['name_oz'],
                        'price': price,
                        'link': f"https://olcha.uz/oz/product/view/{product['alias']}/",
                        'image_link': product['main_image']
                    }
                )
            
            def get_price(API):
                price = API.get('price', '0')
                return float(price)
            
            API.sort(key=get_price, reverse=False)
            return API
        else:
            return ("Olchda mahsulot topilmadi,", status.HTTP_404_NOT_FOUND )
    else:
        return ("Status code:", response.status_code)

def texnomart(encoded_query, texnomart_api_link):
    
    headers = {
        "Accept-Language": "oz"
    }
    response = requests.get(f"{texnomart_api_link}{encoded_query}&sort=&page=1")
    
    if response.status_code == 200:  
        data = response.json() 
        products = data['data']['products'][0:5]
        API = []
        
        if products:
            for product in products:
                
                if product['sale_price']:
                    price = product['sale_price']
                else:
                    price = product['loan_price']
                API.append(
                    {
                        'name': product['name'],
                        'price': price,
                        'link': f"https://texnomart.uz/product/detail/{product['id']}",
                        'image_link': product['image']
                    }
                )
            
            def get_price(API):
                price = API.get('price', '0')
                return float(price)
            
            API.sort(key=get_price, reverse=False)
            return API
        else:
            return ("Mahsulot topilmadi,", status.HTTP_404_NOT_FOUND )
    else:
        return ("Status code:", response.status_code)


class SearchProductView(APIView):
    def get(self, request):
        product_name = request.GET.get('query')
        encoded_query = quote(product_name)
        if encoded_query:

            result_zoodmall = zoodmall(encoded_query, zoodmall_api_link=zoodmall_api_link)
            result_sello = sello(encoded_query, sello_api_link=sello_api_link)
            result_olcha = olcha(encoded_query, olcha_api_link=olcha_api_link)
            result_texnomart = texnomart(encoded_query, texnomart_api_link=texnomart_api_link)
            
            return Response({"products": {
                "zoodmall": result_zoodmall,
                "sello": result_sello,
                "olcha": result_olcha,
                "texnomart": result_texnomart
            } })
        else:
            return Response({"message": "Product name not provided."})
