from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from urllib.parse import quote
from data.data import zoodmall_api_link, sello_api_link, olcha_api_link, texnomart_api_link, korrektor_token

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote


from .renderers import UserRenderer
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdminUserOrReadOnly
from .throttles import CustomBearerTokenRateThrottle


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("--disable-gpu")

# browser = webdriver.Chrome(options=chrome_options)
def get_all_low_price(allProducts):
    def get_price(allProducts):
        price = allProducts.get('price', '0')
        return float(price)

    allProducts.sort(key=get_price, reverse=False)
    return allProducts


def uzum(encoded_query, allProducts):
    cookie_string ="_gcl_au=1.1.1126409477.1692954200; _ym_uid=1692954201826510623; _ym_d=1692954201; tmr_lvid=dc19ff24c244eaeb0b692aa75568caa2; tmr_lvidTS=1692954201019; _ga_RHGS2343RN=GS1.1.1693758930.1.0.1693758950.40.0.0; _gac_UA-235641814-1=1.1693759116.CjwKCAjw3dCnBhBCEiwAVvLcu9OaizA8Hor87bxHnSpPWHWXXIxRXvf_qo4pKroEfsJZRrQv7Uq3UxoCK0sQAvD_BwE; _gcl_aw=GCL.1693759116.CjwKCAjw3dCnBhBCEiwAVvLcu9OaizA8Hor87bxHnSpPWHWXXIxRXvf_qo4pKroEfsJZRrQv7Uq3UxoCK0sQAvD_BwE; uzum-customers=2b752e6686aab24cef51c33c5267da31|480c8e27df8fb2794d4d4e35bad9c66c; cf_clearance=5ynHMyT2waEd8Xf0v2zlP0Pm9fnc1hU95TWudLo8fXM-1700238205-0-1-7573300d.ec035a4e.22726fed-0.2.1700238205; access_token=eyJraWQiOiIwcE9oTDBBVXlWSXF1V0w1U29NZTdzcVNhS2FqYzYzV1N5THZYb0ZhWXRNIiwiYWxnIjoiRWREU0EiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJVenVtIElEIiwiaWF0IjoxNzAwNDAyMzcwLCJzdWIiOiI4NGU1MTljNS04YTFhLTQ5OTgtOTNkMC01MzFkYjM1ZDk1MTYiLCJhdWQiOlsidXp1bV9hcHBzIiwibWFya2V0L3dlYiJdLCJldmVudHMiOnt9LCJleHAiOjE3MDA0MDMwOTB9.WHQUPveqtUjt3HNHinpUQYrP_LkykVykJRW2q-iq0Aa-TmB6W6aWgcgLAisjStaMAdrA1NYFenw9dpkGQwgOCg; _gid=GA1.2.136165838.1700402527; _ga=GA1.1.1521422407.1692954200; _ym_isad=1; _ym_visorc=b; tmr_detect=0%7C1700402530475; _ga_EZ8RKY9S93=GS1.2.1700402530.32.0.1700402530.0.0.0; _ga_7KCSSWWYYD=GS1.1.1700402379.38.1.1700402532.34.0.0"
    # cookie_string = "_gcl_au=1.1.1126409477.1692954200; _ym_uid=1692954201826510623; _ym_d=1692954201; tmr_lvid=dc19ff24c244eaeb0b692aa75568caa2; tmr_lvidTS=1692954201019; _ga_RHGS2343RN=GS1.1.1693758930.1.0.1693758950.40.0.0; _gac_UA-235641814-1=1.1693759116.CjwKCAjw3dCnBhBCEiwAVvLcu9OaizA8Hor87bxHnSpPWHWXXIxRXvf_qo4pKroEfsJZRrQv7Uq3UxoCK0sQAvD_BwE; _gcl_aw=GCL.1693759116.CjwKCAjw3dCnBhBCEiwAVvLcu9OaizA8Hor87bxHnSpPWHWXXIxRXvf_qo4pKroEfsJZRrQv7Uq3UxoCK0sQAvD_BwE; _gid=GA1.2.805844873.1700220645; _ym_isad=1; uzum-customers=2b752e6686aab24cef51c33c5267da31|480c8e27df8fb2794d4d4e35bad9c66c; _ym_visorc=b; access_token=eyJraWQiOiIwcE9oTDBBVXlWSXF1V0w1U29NZTdzcVNhS2FqYzYzV1N5THZYb0ZhWXRNIiwiYWxnIjoiRWREU0EiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJVenVtIElEIiwiaWF0IjoxNzAwMjM4MTgyLCJzdWIiOiI4NGU1MTljNS04YTFhLTQ5OTgtOTNkMC01MzFkYjM1ZDk1MTYiLCJhdWQiOlsidXp1bV9hcHBzIiwibWFya2V0L3dlYiJdLCJldmVudHMiOnt9LCJleHAiOjE3MDAyMzg5MDJ9.naqKhZgWuLFKyQTkS0SI_8UY1TogtkUE2YaIVRK8HtxCgXkK6W0KLmT1rY3_cRVFVC6_ZcFhaEuQ-cjcei3WAw; _gat_UA-235641814-1=1; _ga=GA1.2.1521422407.1692954200; tmr_detect=1%7C1700238196332; _ga_7KCSSWWYYD=GS1.1.1700236624.36.1.1700238196.40.0.0; cf_clearance=Dqt4KEa_wyV8bLaEcNo06._93UXGHiNE1oCbqpSl_G8-1700238200-0-1-7573300d.ec035a4e.22726fed-0.2.1700238200; _ga_EZ8RKY9S93=GS1.2.1700236639.31.1.1700238197.0.0.0"
    browser.add_cookie({'name': 'cookie_name', 'value': cookie_string, 'domain': 'uzum.uz'})
    browser.get(f"https://uzum.uz/uz/search?query={encoded_query}&needsCorrection=1")
    print(f"https://uzum.uz/uz/search?query={encoded_query}&needsCorrection=1")
    print(browser.page_source)
    wait = WebDriverWait(browser, 30)

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ui-card")))

    uzum_page = browser.page_source
    uzum_soup = BeautifulSoup(uzum_page, "lxml")
    
    
    product_check = uzum_soup.find("div", attrs={"id":"category-products"})
    
    if product_check:

        uzum_products_data = uzum_soup.find("div", attrs={"id":"category-products"})

        uzum_products = uzum_products_data.find_all("div", attrs={'data-test-id':"item__product-card"})

        uzum_products = uzum_products[0:5]
        
        products = []
        
        for product in uzum_products:
            uzum_pr_block = product.find("a", attrs={"class":"subtitle-item"})
            uzum_pr_image = product.find("img", attrs={"class":"main-card-icon-and-classname-collision-made-to-minimum"}).get('src')
            uzum_pr_name = uzum_pr_block.text.strip()
            uzum_pr_link = uzum_pr_block.get('href')

            
            
            uzum_pr_price = product.find("span",attrs={"class":"currency product-card-price slightly medium"}).text.strip().replace('\xa0', ' ').replace(' ', '').replace(',', ' ').replace("so'm", "")
            products.append(
                {
                    'name': uzum_pr_name,
                    'price': int(uzum_pr_price),
                    'link': "https://uzum.uz"+uzum_pr_link,
                    'image_link': uzum_pr_image
                }
            )

            allProducts.append(
                {
                    'name': uzum_pr_name,
                    'price': int(uzum_pr_price),
                    'link': "https://uzum.uz"+uzum_pr_link,
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
     
def zoodmall(encoded_query, zoodmall_api_link, allProducts):
    
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
                        'price': product['localPrice'],
                        'link': f"https://www.zoodmall.uz/product/{product['productId']}/",
                        'image_link': product['imgUrl']
                    }
                )
                
                allProducts.append(
                    {
                        'name': product['name'],
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
            return ("Zoodmallda bunday mahsulot topilmadi,", status.HTTP_204_NO_CONTENT )   
    else:
        print("Status code", response.status_code)
               
def asaxiy(encoded_query, allProducts):
    
    url = f'https://asaxiy.uz/uz/product/sort=rate-high?key={encoded_query}'
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.content
        asaxiy_soup = BeautifulSoup(html_content, 'html.parser')
        asaxiy_products = asaxiy_soup.find_all("div", attrs={"class":"product__item d-flex flex-column justify-content-between"})
        asaxiy_products = asaxiy_products[0:5]
        
        products = []
        
        
        for product in asaxiy_products:

            asaxiy_pr_name = product.find("span", attrs={"class":"product__item__info-title"}).text.strip()
            asaxiy_pr_link = product.find("a").get('href')
            asaxiy_pr_image = product.find("img", attrs={"class":"img-fluid lazyload"}).get('data-src')
            asaxiy_pr_price = product.find("span",attrs={"class":"product__item-price"}).text.strip()[0:-4].replace(' ', '')
               
            products.append(
                {
                    'name': asaxiy_pr_name,
                    'price': int(asaxiy_pr_price),
                    'link': "https://www.asaxiy.uz"+asaxiy_pr_link,
                    'image_link': asaxiy_pr_image
                }
            )

            allProducts.append(
                {
                    'name': asaxiy_pr_name,
                    'price': int(asaxiy_pr_price),
                    'link': "https://www.asaxiy.uz"+asaxiy_pr_link,
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
        print(f'Asaxiy mahsulot topilmadi, {response.status_code}')

    
def sello(encoded_query, sello_api_link, allProducts):
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Fingerprint": "10b4ad6ce60f51511b502f34c14f8966",
        "Language": "uz" 
    }
    response = requests.get(f"{sello_api_link}{encoded_query}&page=1&perPage=30&sortBy=price_asc", headers=headers)
    
    
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
                
                allProducts.append(
                    {
                        'name': product['name'],
                        'price': price,
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
            return ("Selloda mahsulot topilmadi,", status.HTTP_204_NO_CONTENT )
    else:
        return ("Status code:", response.status_code)
        
def olcha(encoded_query, olcha_api_link, allProducts):
    
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

                allProducts.append(
                    {
                        'name': product['name_oz'],
                        'price': price,
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
            return ("Olchada mahsulot topilmadi,", status.HTTP_204_NO_CONTENT )
    else:
        return ("Status code:", response.status_code)

def texnomart(encoded_query, texnomart_api_link, allProducts):
    
    headers = {
        "Accept-Language": "uz"
    }
    response = requests.get(f"{texnomart_api_link}{encoded_query}&sort=&page=1", headers=headers)
    
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
                
                low_price = get_all_low_price(allProducts=allProducts)
                
                if price < low_price['products']['all'][0]['price']:
                    pass
                else:
                    API.append(
                        {
                            'name': product['name'],
                            'price': price,
                            'link': f"https://texnomart.uz/product/detail/{product['id']}",
                            'image_link': product['image']
                        }
                    )
                    
                    allProducts.append(
                        {
                            'name': product['name'],
                            'price': price,
                            'link': f"https://texnomart.uz/product/detail/{product['id']}",
                            'image_link': product['image'],
                            'market_place': "texnomart.uz"
                        }
                    )
            
            def get_price(API):
                price = API.get('price', '0')
                return float(price)
            
            API.sort(key=get_price, reverse=False)
            return API
        else:
            return ("Mahsulot topilmadi,", status.HTTP_204_NO_CONTENT )
    else:
        return ("Status code:", response.status_code)



class SearchProductView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]
    throttle_classes = [CustomBearerTokenRateThrottle]
    def get(self, request):
        allProducts = []
        product_name = request.GET.get('query')
        encoded_query = quote(product_name)
        if encoded_query:

            # try:
            #     result_uzum = uzum(encoded_query=encoded_query, allProducts=allProducts)
            # except Exception as e:
            #     result_uzum = "ERROR: " + str(e)
            #     print(e)
            
            try:
                result_asaxiy = asaxiy(encoded_query=encoded_query, allProducts=allProducts)
            except Exception as e:
                result_asaxiy = "ERROR: " + str(e)
                print(e)
                
            try:
                result_zoodmall = zoodmall(encoded_query, zoodmall_api_link=zoodmall_api_link, allProducts=allProducts)
            except Exception as e:
                result_zoodmall = "ERROR: " + str(e)
                print(e)

            try:
                result_sello = sello(encoded_query, sello_api_link=sello_api_link, allProducts=allProducts)
            except Exception as e:
                result_sello = "ERROR: " + str(e)
                print(e)

            try:
                result_olcha = olcha(encoded_query, olcha_api_link=olcha_api_link, allProducts=allProducts)
            except Exception as e:
                result_olcha = "ERROR: " + str(e)
                print(e)

            try:
                result_texnomart = texnomart(encoded_query, texnomart_api_link=texnomart_api_link, allProducts=allProducts)
            except Exception as e:
                result_texnomart = "ERROR: " + str(e)
                print(e)

            try:
                result_all = get_all_low_price(allProducts=allProducts)
            except Exception as e:
                result_all = "ERROR: " + str(e)
                print(e)
            
            try:
                return Response({
                "products": {
                    # "uzum": result_uzum,
                    "asaxiy": result_asaxiy,
                    "zoodmall": result_zoodmall,
                    "sello": result_sello,
                    "olcha": result_olcha,
                    "texnomart": result_texnomart
                }, 
                "all": result_all
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
