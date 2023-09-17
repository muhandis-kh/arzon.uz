import requests
from urllib.parse import quote
from pprint import pprint
from bs4 import BeautifulSoup
from colorama import Fore, Style
from rest_framework import status

mahsulot_nomi = input("Mahsulot nomini kiriting: ")
encoded_query = quote(mahsulot_nomi)

def uzum(encoded_query):

    encoded_query = quote(mahsulot_nomi)
    response = requests.get(f"https://api.uzum.uz/api/search?query={encoded_query}&needsCorrection=1")

    if response.status_code == 200:
        data = response.json()
        pprint(data['marketList'][0:5])
    else:
        print("İstek başarısız oldu. Durum kodu:", response.status_code)

def zoodmall(encoded_query):
    
    url = f"https://www.zoodmall.uz/api/getproducts-list?deviceType=web&nocache=true&&rowsPerPage=48&categoryId=0&nameLike={encoded_query}&page=1&sort=1"
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
            pprint(API)
            print(Fore.GREEN + "***********************************************************************************************************************")
            print(Style.RESET_ALL)
        else:
            print("Mahsulot topilmadi,", status.HTTP_404_NOT_FOUND )    
    else:
        print("İstek başarısız oldu. Durum kodu:", response.status_code)
        
def sello(encoded_query):
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Fingerprint": "10b4ad6ce60f51511b502f34c14f8966",
        "Language": "uz" 
    }
    response = requests.get(f"https://stg-api.sello.uz/algolia/search?query={encoded_query}&page=1&perPage=30", headers=headers)
    
    
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
            pprint(API)
        else:
            print("Mahsulot topilmadi,", status.HTTP_404_NOT_FOUND )
    else:
        print("İstek başarısız oldu. Durum kodu:", response.status_code)
        
def olcha(encoded_query):
    
    headers = {
        "Accept-Language": "oz"
    }
    response = requests.get(f"https://mobile.olcha.uz/api/v2/products?q={encoded_query}", headers=headers)
    
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
            pprint(API)
        else:
            print("Mahsulot topilmadi,", status.HTTP_404_NOT_FOUND )
    else:
        print("İstek başarısız oldu. Durum kodu:", response.status_code)

def texnomart(encoded_query):
    
    headers = {
        "Accept-Language": "oz"
    }
    response = requests.get(f"https://gateway.texnomart.uz/api/common/v1/search/result?q={encoded_query}&sort=&page=1")
    
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
            pprint(API)
        else:
            print("Mahsulot topilmadi,", status.HTTP_404_NOT_FOUND )
    else:
        print("İstek başarısız oldu. Durum kodu:", response.status_code)

def elmakon(encoded_query=encoded_query):
    url = f"https://elmakon.uz/uz/?match=all&subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&q={encoded_query}&dispatch=products.search&security_hash=5456105ab804c2d4bc3604c473676433"
    request = requests.get(url)
    response = request.text
    soup = BeautifulSoup(response, 'html.parser')
    script_tags = soup.find_all("script")
    for script_tag in script_tags:
        print(script_tag.text)
        # script_data = script_tag.text
        # print(script_data)
    # if response.status_code == 200:  
    #     data = response.content
    #     pprint(data)
        # products = data['data']['products'][0:5]
        # API = []
        
        # if products:
        #     for product in products:
                
        #         if product['sale_price']:
        #             price = product['sale_price']
        #         else:
        #             price = product['loan_price']
        #         API.append(
        #             {
        #                 'name': product['name'],
        #                 'price': price,
        #                 'link': f"https://texnomart.uz/product/detail/{product['id']}",
        #                 'image_link': product['image']
        #             }
        #         )
            
        #     def get_price(API):
        #         price = API.get('price', '0')
        #         return float(price)
            
        #     API.sort(key=get_price, reverse=False)
        #     pprint(API)
        # else:
        #     print("Mahsulot topilmadi,", status.HTTP_404_NOT_FOUND )
    # else:
    #     print("İstek başarısız oldu. Durum kodu:", response.status_code)

    
# zoodmall()
# sello()
# olcha()
# texnomart()
elmakon()

# https://api.uzum.uz/api/v2/product/search?query=asus