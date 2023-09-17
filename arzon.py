from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from pprint import pprint

# 10 saniye boyunca, belirtilen öğenin görünür olmasını bekler



chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")

browser = webdriver.Chrome(options=chrome_options)



mahsulot_nomi = input("Mahsulot nomini kiriting: ")

def uzum():

    encoded_query = quote(mahsulot_nomi)

    browser.get(f"https://uzum.uz/uz/search?query={encoded_query}&needsCorrection=1")
    wait = WebDriverWait(browser, 30)

    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "card-info-block")))
   
    uzum_page = browser.page_source
    uzum_soup = BeautifulSoup(uzum_page, "lxml")
    
    
    product_check = uzum_soup.find("div", attrs={"id":"category-header"})
    
    if product_check:

        uzum_products_data = uzum_soup.find("div", attrs={"id":"category-content"})

        uzum_products = uzum_products_data.find_all("div", attrs={"class":"ui-card"})

        uzum_products = uzum_products[0:5]
        
        products = []
        
        for product in uzum_products:
            uzum_pr_block = product.find("a", attrs={"class":"subtitle-item"})
            uzum_pr_image = product.find("img", attrs={"class":"main-card-icon-and-classname-collision-made-to-minimum"}).get('src')
            uzum_pr_name = uzum_pr_block.text.strip()
            uzum_pr_link = uzum_pr_block.get('href')

            uzum_pr_price = product.find("span",attrs={"class":"currency product-card-price slightly medium"}).text.strip()
            products.append(
                {
                    'name': uzum_pr_name,
                    'price': uzum_pr_price.replace('\xa0', ' ').replace(' ', ' ').replace(',', ' '),
                    'link': "https://uzum.uz"+uzum_pr_link,
                    'image_link': uzum_pr_image
                }
            )
        
        
        def get_price(products):
            price_str = products.get('price', '0')
            
            return float(price_str[0:-5].replace(" ", ""))
        
        products.sort(key=get_price, reverse=False)
        pprint(products)

    else:
        print("Bunday mahsulot topilmadi")
     
def olcha():

    encoded_query = quote(mahsulot_nomi)

    browser.get(f"https://www.olcha.uz/search?q={encoded_query}")
    wait = WebDriverWait(browser, 30)

    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shop-content__item")))

    olcha_page = browser.page_source
    olcha_soup = BeautifulSoup(olcha_page, "lxml")
    
    product_check = olcha_soup.find("div", attrs={"class":"shop-content__item"}).find("div", attrs={"class":"h2"}).text.find(" 0 ")
    if product_check == -1:
        
    
        olcha_products = olcha_soup.find_all("div", attrs={"class":"product-card _big _slider"})
        olcha_products = olcha_products[0:5]
        
        products = []
        
        for product in olcha_products:
            olcha_pr_name = product.find("div", attrs={"class":"product-card__brand-name"}).text.strip()
            olcha_pr_link = product.find("a", attrs={"class":"product-card__col"}).get('href')
            olcha_pr_image = product.find("div", attrs={"class":"slide"}).find('a').find("img").get('src')
            olcha_pr_price = product.find("div",attrs={"class":"price__main"}).text.strip()
            
            products.append(
                {
                    'name': olcha_pr_name,
                    'price': olcha_pr_price,
                    'link': "https://www.olcha.uz/uz"+olcha_pr_link[3:],
                    'image_link': olcha_pr_image
                }
            )
        
        def get_price(products):
            price_str = products.get('price', '0')
            
            return float(price_str[0:-4].replace(" ", ""))
        
        products.sort(key=get_price, reverse=False)
        pprint(products)

    else:
        print("Bunday mahsulot topilmadi")
    
 
def zoodmall():
    encoded_query = quote(mahsulot_nomi)

    browser.get(f"https://www.zoodmall.uz/search/?q={encoded_query}")
    wait = WebDriverWait(browser, 30)

    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "productList-container")))

    zoodmall_page = browser.page_source
    zoodmall_soup = BeautifulSoup(zoodmall_page, "lxml")
    
    product_check = zoodmall_soup.find("div", attrs={"class":"productlist-catalog el-row is-align-middle el-row--flex"})
    if product_check:
        
    
        zoodmall_products = zoodmall_soup.find_all("div", attrs={"class":"product-item-list el-col el-col-24 el-col-xs-12 el-col-sm-8 el-col-md-12 el-col-lg-8"})
        zoodmall_products = zoodmall_products[0:5]
        
        products = []
        
        for product in zoodmall_products:
            
            
            zoodmall_pr_name = product.find("div", attrs={"class":"product-mini__title"}).text.strip()
            zoodmall_pr_link = product.find("a", attrs={"class":"product-mini"}).get('href')
            zoodmall_pr_image = product.find("div", attrs={"class":"el-image"}).find("img").get('src')
            zoodmall_pr_price = product.find("div",attrs={"class":"product-mini__totalLocalPrice"})
            
            if zoodmall_pr_price:
                zoodmall_pr_price = zoodmall_pr_price.find('b').text.strip()
            else:
                zoodmall_pr_price = product.find("div",attrs={"class":"product-mini__payment"}).find('b').text.strip()
                
            products.append(
                {
                    'name': zoodmall_pr_name,
                    'price': zoodmall_pr_price,
                    'link': "https://www.zoodmall.uz"+zoodmall_pr_link,
                    'image_link': zoodmall_pr_image
                }
            )
        
        def get_price(products):
            price_str = products.get('price', '0')
            price_str = str(zoodmall_pr_price)[4:].strip().replace(',', '')
            return float(price_str)
        
        products.sort(key=get_price, reverse=False)
        pprint(products)

    else:
        print("Bunday mahsulot topilmadi")
    
 
def asaxiy():

    encoded_query = quote(mahsulot_nomi)

    browser.get(f"https://asaxiy.uz/product/sort=cheap?key={encoded_query}")
    wait = WebDriverWait(browser, 30)

    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product__item.d-flex.flex-column.justify-content-between ")))

    asaxiy_page = browser.page_source
    asaxiy_soup = BeautifulSoup(asaxiy_page, "lxml")
    
    product_check = asaxiy_soup.find("div", attrs={"class":"row custom-gutter mb-40"})
    if product_check:
        
    
        asaxiy_products = asaxiy_soup.find_all("div", attrs={"class":"product__item d-flex flex-column justify-content-between"})
        asaxiy_products = asaxiy_products[0:5]
        
        products = []
        
        
        for product in asaxiy_products:

            asaxiy_pr_name = product.find("span", attrs={"class":"product__item__info-title"}).text.strip()
            asaxiy_pr_link = product.find("a").get('href')
            asaxiy_pr_image = product.find("img", attrs={"class":"img-fluid lazyload"}).get('src')
            asaxiy_pr_price = product.find("span",attrs={"class":"product__item-price"}).text.strip()
               
            products.append(
                {
                    'name': asaxiy_pr_name,
                    'price': asaxiy_pr_price,
                    'link': "https://www.asaxiy.uz"+asaxiy_pr_link,
                    'image_link': asaxiy_pr_image
                }
            )
        
        def get_price(products):
            price_str = products.get('price', '0')
            price_str = str(asaxiy_pr_price)[0:-4].replace(' ', '')
            return float(price_str)
        
        products.sort(key=get_price, reverse=False)
        pprint(products)

    else:
        print("Bunday mahsulot topilmadi")
    
 
def elmakon():

    encoded_query = quote(mahsulot_nomi)

    browser.get(f"https:www.elmakon.uz/?match=all&subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&q={encoded_query}&dispatch=products.search&security_hash=5456105ab804c2d4bc3604c473676433")
    wait = WebDriverWait(browser, 30)

    element = wait.until(EC.visibility_of_element_located((By.ID, "products_search_pagination_contents")))

    elmakon_page = browser.page_source
    elmakon_soup = BeautifulSoup(elmakon_page, "lxml")
    
    product_check = elmakon_soup.find("div", attrs={"id":"products_search_pagination_contents"})
    if product_check:
        
    
        elmakon_products = elmakon_soup.find_all("div", attrs={"class":"ty-column4"})
        elmakon_products = elmakon_products[0:5]
        
        products = []
        
        
        for product in elmakon_products:

            elmakon_pr_name = product.find("div", attrs={"class":"ut2-gl__name"}).find('a').get('title').strip()
            elmakon_pr_link = product.find('div', attrs={"class": "ut2-gl__image"}).find("a").get('href')
            elmakon_pr_image = product.find("div", attrs={"class": "ut2-gl__image"}).find('a').find('img').get('src')
            elmakon_pr_price = product.find("span",attrs={"class":"ty-price-num"}).text.strip()
               
            products.append(
                {
                    'name': elmakon_pr_name,
                    'price': elmakon_pr_price,
                    'link': elmakon_pr_link,
                    'image_link': elmakon_pr_image
                }
            )
        
        def get_price(products):
            price_str = products.get('price', '0')
            price_str = str(elmakon_pr_price).replace('.', '')
            return float(price_str)
        
        products.sort(key=get_price, reverse=False)
        pprint(products)

    else:
        print("Bunday mahsulot topilmadi")
    
 
def sello():

    encoded_query = quote(mahsulot_nomi)
    response = requests.get(f"https://stg-api.sello.uz/algolia/search?query={encoded_query}&page=1&perPage=30")
    data = response.json()
    pprint(data)
    # browser.get(f"https://stg-api.sello.uz/algolia/search?query={encoded_query}&page=1&perPage=30")
    # wait = WebDriverWait(browser, 30)

    # element = wait.until(EC.visibility_of_element_located((By.ID, "products_search_pagination_contents")))

    # sello_page = browser.page_source
    # sello_soup = BeautifulSoup(sello_page, "lxml")
    
    # product_check = sello_soup.find("div", attrs={"id":"products_search_pagination_contents"})
    # if product_check:
        
    
    #     sello_products = sello_soup.find_all("div", attrs={"class":"ty-column4"})
    #     sello_products = sello_products[0:5]
        
    #     products = []
        
        
    #     for product in sello_products:

    #         sello_pr_name = product.find("div", attrs={"class":"ut2-gl__name"}).find('a').get('title').strip()
    #         sello_pr_link = product.find('div', attrs={"class": "ut2-gl__image"}).find("a").get('href')
    #         sello_pr_image = product.find("div", attrs={"class": "ut2-gl__image"}).find('a').find('img').get('src')
    #         sello_pr_price = product.find("span",attrs={"class":"ty-price-num"}).text.strip()
               
    #         products.append(
    #             {
    #                 'name': sello_pr_name,
    #                 'price': sello_pr_price,
    #                 'link': sello_pr_link,
    #                 'image_link': sello_pr_image
    #             }
    #         )
        
    #     def get_price(products):
    #         price_str = products.get('price', '0')
    #         price_str = str(sello_pr_price).replace('.', '')
    #         return float(price_str)
        
    #     products.sort(key=get_price, reverse=False)
    #     pprint(products)

    # else:
    #     print("Bunday mahsulot topilmadi")
    

uzum()
# olcha()
# zoodmall()
# asaxiy()
# elmakon()
# sello()