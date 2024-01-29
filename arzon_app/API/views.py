from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from urllib.parse import quote
from data.data import zoodmall_api_link, sello_api_link, olcha_api_link, texnomart_api_link, korrektor_token
import httpx

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote, unquote

import random
from .renderers import UserRenderer
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdminUserOrReadOnly
from .throttles import CustomBearerTokenRateThrottle
from .config import json_data, list_headers
from pprint import pprint
import json
import aiohttp
import asyncio

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("--disable-gpu")

# browser = webdriver.Chrome(options=chrome_options)

# Barcha mahsulotlar ichidan narxi bo'yicha o'sib borish tartibida saralash uchun filter
def get_all_low_price(allProducts):
    def get_price(allProducts):
        price = allProducts.get('price', '0')
        return float(price)

    allProducts.sort(key=get_price, reverse=False)
    return allProducts


def uzum(encoded_query, allProducts):
    products = []
    offset = 0

    session = requests.Session()
    response = session.post(
        'https://graphql.uzum.uz/',
        headers=list_headers,
        json=json_data(
            encoded_query,
            offset)).json()
    # async with aiohttp.ClientSession() as session:
    #     response = await session.post(
    #         'https://graphql.uzum.uz/',
    #         headers=list_headers,
    #         json=json_data(encoded_query, offset)
    #     )
    #     data = await response.json()
    try:
        uzum_page = response.get('data').get('makeSearch')
    except:
        uzum_page = False
    if uzum_page:
        
        data = uzum_page['items']
        searching_products = []

        for product in data:
            item = product['catalogCard']
            uzum_pr_name = item['title']
            if encoded_query.lower() in uzum_pr_name.lower():
                searching_products.append(product)
            
        if searching_products:
            for item in searching_products[0:5]:
                item = item['catalogCard']
                uzum_pr_name = item['title']
                uzum_pr_old_price = item['minFullPrice'] if item['minFullPrice'] else None
                uzum_pr_min_price = item['minSellPrice']
                uzum_pr_link = item['productId']
                uzum_pr_image = item['photos'][0]['link']['high']
                products.append(
                    {
                        'name': uzum_pr_name,
                        'old_price': uzum_pr_old_price,
                        'price': uzum_pr_min_price,
                        'link': f"https://uzum.uz/uz/product/{uzum_pr_link}",
                        'image_link': uzum_pr_image
                    }
                )

                allProducts.append(
                    {
                        'name': uzum_pr_name,
                        'old_price': uzum_pr_old_price,
                        'price': uzum_pr_min_price,
                        'link': f"https://uzum.uz/uz/product/{uzum_pr_link}",
                        'image_link': uzum_pr_image,
                        'market_place': "uzum.uz"
                    }
                )
                
            
            def get_price(products):
                price_str = products.get('price', '0')
                
                return float(price_str)
            
            products.sort(key=get_price, reverse=False)
            
            return products
        else:
            return ("Uzumda bunday mahsulot topilmadi,", status.HTTP_204_NO_CONTENT )   

    else:
        return ("Uzumda bunday mahsulot topilmadi,", status.HTTP_204_NO_CONTENT )   
     
async def zoodmall_async(encoded_query, zoodmall_api_link, allProducts):
    url = f"{zoodmall_api_link}{encoded_query}&page=1&sort=1"

    headers = {
        "x-lang": "uz",
        "x-marketcode": "UZ"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                products = data['marketList']
                searching_products = [product for product in products if unquote(encoded_query) in product['name'].lower()]

                API = []

                if products:
                    searching_products = searching_products if searching_products else products
                    for product in searching_products[0:5]:
                        if product['localCrossedPrice']:
                            old_price = product['localCrossedPrice'] if product['localCrossedPrice'] > product['localPrice'] else None
                        else:
                            old_price = None

                        API.append(
                            {
                                'name': product['name'],
                                'old_price': old_price,
                                'price': product['localPrice'],
                                'link': f"https://www.zoodmall.uz/product/{product['productId']}/",
                                'image_link': product['imgUrl']
                            }
                        )

                        allProducts.append(
                            {
                                'name': product['name'],
                                'old_price': old_price,
                                'price': product['localPrice'],
                                'link': f"https://www.zoodmall.uz/product/{product['productId']}/",
                                'image_link': product['imgUrl'],
                                'market_place': "zoodmall.uz"
                            }
                        )

                    def get_price(API):
                        price = API.get('price', '0')
                        return float(price)

                    API.sort(key=get_price, reverse=False)
                    return API
                else:
                    return ("Zoodmallda bunday mahsulot topilmadi,", status.HTTP_204_NO_CONTENT)
            else:
                print("Status code", response.status)
   
async def fetch_asaxiy(session, url):
    async with session.get(url) as response:
        return await response.text()

async def asaxiy_async(encoded_query, allProducts):
    user_agent_list = [
        #Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
        ]

    url = f'http://asaxiy.uz/uz/product/sort=rate-high?key={encoded_query}'

    headers = {
        "User-Agent": random.choice(user_agent_list)
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        html_content = await fetch_asaxiy(session, url)

        if html_content:
            asaxiy_soup = BeautifulSoup(html_content, 'lxml')
            asaxiy_products = asaxiy_soup.find_all("div", attrs={"class": "product__item d-flex flex-column justify-content-between"})
            asaxiy_products = asaxiy_products

            products = []

            product_check = asaxiy_soup.find("div", attrs={"class": "row custom-gutter mb-40"})
            if product_check:
                searching_products = []

                for product in asaxiy_products:
                    asaxiy_pr_name = product.find("span", attrs={"class": "product__item__info-title"}).text.strip()
                    if unquote(encoded_query).lower() in asaxiy_pr_name.lower():
                        searching_products.append(product)
                
                
                if searching_products:
                    for product in searching_products[0:5]:
                        asaxiy_pr_name = product.find("span", attrs={"class": "product__item__info-title"}).text.strip()
                        for a in product.find_all('a', href=True):
                            if a['href'].startswith('/uz/product'):
                                asaxiy_pr_link = a['href']
                            else:
                                None

                        asaxiy_pr_image = product.find("img", attrs={"class": "img-fluid lazyload"}).get('data-src')
                        try:
                            asaxiy_pr_old_price = product.find("span", attrs={"class": "product__item-old--price"}).text.strip()[0:-4].replace(' ', '')
                        except Exception as e:
                            asaxiy_pr_old_price = None
                        asaxiy_pr_price = product.find("span", attrs={"class": "product__item-price"}).text.strip()[0:-4].replace(' ', '')

                        products.append(
                            {
                                'name': asaxiy_pr_name,
                                'old_price': int(asaxiy_pr_old_price) if asaxiy_pr_old_price else None,
                                'price': int(asaxiy_pr_price),
                                'link': "https://www.asaxiy.uz" + asaxiy_pr_link if asaxiy_pr_link else None,
                                'image_link': asaxiy_pr_image
                            }
                        )

                        allProducts.append(
                            {
                                'name': asaxiy_pr_name,
                                'old_price': int(asaxiy_pr_old_price) if asaxiy_pr_old_price else None,
                                'price': int(asaxiy_pr_price),
                                'link': "https://www.asaxiy.uz" + asaxiy_pr_link,
                                'image_link': asaxiy_pr_image,
                                'market_place': "asaxiy.uz"
                            }
                        )

                    def get_price(products):
                        price_str = products.get('price', '0')
                        return float(price_str)

                    products.sort(key=get_price, reverse=False)

                    return products
                else:
                    return ("Asaxiyda mahsulot topilmadi,", status.HTTP_204_NO_CONTENT)
                    
            else:
                return ("Asaxiyda mahsulot topilmadi,", status.HTTP_204_NO_CONTENT)
        else:
            print('Asaxiy mahsulot topilmadi, HTTP istek hatası')

async def fetch_sello(session, url):
    async with session.get(url) as response:
        return await response.text()

async def sello_async(encoded_query, sello_api_link, allProducts):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"{sello_api_link}{encoded_query}&page=1&perPage=30&sortBy=name_desc"
        html_content = await fetch_sello(session, url)

        if html_content:
            data = json.loads(html_content) 
            products = data['hits'][0:5]
            API = []

            if products:
                for product in products:
                    if product['discounted_price']:
                        sello_pr_price = product['discounted_price']
                    else:
                        sello_pr_price = product['price']

                    API.append(
                        {
                            'name': product['name'],
                            'old_price': product['price'] if sello_pr_price < product['price'] else None,
                            'price': sello_pr_price, 
                            'link': f"https://sello.uz/uz/product/{product['slug']}/",
                            'image_link': f"https://static.sello.uz/unsafe/x500/https://static.sello.uz{product['imageURL']}"
                        }
                    )

                    allProducts.append(
                        {
                            'name': product['name'],
                            'old_price': product['price'] if sello_pr_price < product['price'] else None,
                            'price': sello_pr_price,
                            'link': f"https://sello.uz/uz/product/{product['slug']}/",
                            'image_link': f"https://static.sello.uz/unsafe/x500/https://static.sello.uz{product['imageURL']}",
                            'market_place': "sello.uz"
                        }
                    )

                def get_price(API):
                    price = API.get('price', '0')
                    return float(price)

                API.sort(key=get_price, reverse=False)

                return API
            else:
                return ("Selloda mahsulot topilmadi,", status.HTTP_204_NO_CONTENT)
        else:
            print('Sello mahsulot topilmadi, HTTP istek hatası')

async def fetch_olcha(session, url):
    async with session.get(url) as response:
        return await response.json()

async def olcha_async(encoded_query, olcha_api_link, allProducts):
    headers = {
        "Accept-Language": "oz"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"{olcha_api_link}{encoded_query}"
        html_content = await fetch_olcha(session, url)

        if html_content:
            data = html_content
            products = data['data']['products'][0:5]
            API = []

            if products:
                for product in products:
                    if product['discount_price']:
                        price = product['discount_price']
                    else:
                        price = product['total_price']
                    total_price = int(product['total_price'])
                    API.append(
                        {
                            'name': product['name_oz'],
                            'old_price': total_price if price > total_price else None,
                            'price': int(price),
                            'link': f"https://olcha.uz/oz/product/view/{product['alias']}/",
                            'image_link': product['main_image']
                        }
                    )

                    allProducts.append(
                        {
                            'name': product['name_oz'],
                            'old_price': total_price if price > total_price else None,
                            'price': int(price),
                            'link': f"https://olcha.uz/oz/product/view/{product['alias']}/",
                            'image_link': product['main_image'],
                            'market_place': "olcha.uz"
                        }
                    )

                def get_price(API):
                    price = API.get('price', '0')
                    return float(price)

                API.sort(key=get_price, reverse=False)

                return API
            else:
                return ("Olchada mahsulot topilmadi,", status.HTTP_204_NO_CONTENT)
        else:
            print('Olcha mahsulot topilmadi, HTTP istek hatası')

async def fetch_texnomart(session, url):
    async with session.get(url) as response:
        return await response.json()

async def texnomart_async(encoded_query, texnomart_api_link, allProducts):
    headers = {
        "Accept-Language": "uz"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"{texnomart_api_link}{encoded_query}&sort=&page=1"
        data = await fetch_texnomart(session, url)

        products = data['data']['products']
        searching_products = []

        for product in products:
            if unquote(encoded_query).lower() in product['name'].lower():
                searching_products.append(product)

        API = []
        
        searching_products = searching_products if searching_products else products
        if searching_products:
            for product in searching_products[0:5]:
                price = product['sale_price'] if product['sale_price'] else product['old_price']
                low_price = get_all_low_price(allProducts=allProducts)

                if low_price:
                    if price < low_price[0]['price']:
                        pass
                    else:
                        API.append(
                            {
                                'name': product['name'],
                                'old_price': product['old_price'],
                                'price': price,
                                'link': f"https://texnomart.uz/product/detail/{product['id']}",
                                'image_link': product['image']
                            }
                        )

                        allProducts.append(
                            {
                                'name': product['name'],
                                'old_price': product['old_price'],
                                'price': product['sale_price'] if product['sale_price'] else product['old_price'],
                                'link': f"https://texnomart.uz/product/detail/{product['id']}",
                                'image_link': product['image'],
                                'market_place': "texnomart.uz"
                            }
                        )
            if API:
                def get_price(API):
                    price = API.get('price', '0')
                    return float(price)

                API.sort(key=get_price, reverse=False)
                return API
            else:
                return ("Mahsulot topilmadi,", status.HTTP_204_NO_CONTENT)
        else:
            return ("Mahsulot topilmadi,", status.HTTP_204_NO_CONTENT)
    

async def main(product_name, allProducts):

        
        try:
            result_asaxiy = await asaxiy_async(encoded_query=product_name, allProducts=allProducts)
        except Exception as e:
            result_asaxiy = "ERROR: " + str(e)
            print(e)
            
        try:
            result_zoodmall = await zoodmall_async(product_name, zoodmall_api_link=zoodmall_api_link, allProducts=allProducts)
        except Exception as e:
            result_zoodmall = "ERROR: " + str(e)
            print(e)

        try:
            result_sello = await sello_async(product_name, sello_api_link=sello_api_link, allProducts=allProducts)
        except Exception as e:
            result_sello = "ERROR: " + str(e)
            print(e)

        try:
            result_olcha = await olcha_async(product_name, olcha_api_link=olcha_api_link, allProducts=allProducts)
        except Exception as e:
            result_olcha = "ERROR: " + str(e)
            print(e)

        try:
            result_texnomart = await texnomart_async(product_name, texnomart_api_link=texnomart_api_link, allProducts=allProducts)
        except Exception as e:
            result_texnomart = "ERROR: " + str(e)
            print(e)

        try:
            result_all = get_all_low_price(allProducts=allProducts)
        except Exception as e:
            result_all = "ERROR: " + str(e)
            print(e)
            
        return (result_asaxiy, result_zoodmall, result_olcha, result_sello, result_texnomart, result_all)

class SearchProductView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]
    throttle_classes = [CustomBearerTokenRateThrottle]
    def get(self, request):
        allProducts = []
        product_name = request.GET.get('query')
        encoded_query = quote(product_name)
        if encoded_query:

            results = asyncio.run(main(product_name=encoded_query, allProducts=allProducts))
            try:
                result_uzum = uzum(encoded_query=product_name, allProducts=allProducts)
            except Exception as e:
                result_uzum = "ERROR: " + str(e)
                print(e)
            try:
                return Response({
                "products": {
                    "uzum": result_uzum,
                    "asaxiy": results[0],
                    "zoodmall": results[1],
                    "sello": results[3],
                    "olcha": results[2],
                    "texnomart": results[4]
                }, 
                "all": results[-1]
                                   })
            except Exception as e:
                return Response(f"Error message: {e}")
        else:
            return Response({"message": "Product name not provided."})


""" Authentification Views """
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'message': "Ro'yhatdan muvaffaqiyatli o'tdingiz"}, status=status.HTTP_201_CREATED)
