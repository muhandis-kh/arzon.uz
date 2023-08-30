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

mahsulot_nomi = input("Mahsulot nomini kiriting: ")
encoded_query = quote(mahsulot_nomi)

def uzum():

    encoded_query = quote(mahsulot_nomi)
    response = requests.get(f"https://api.uzum.uz/api/search?query={encoded_query}&needsCorrection=1")

    if response.status_code == 200:
        data = response.json()
        pprint(data['marketList'][0:5])
    else:
        print("İstek başarısız oldu. Durum kodu:", response.status_code)

def zoodmall():
    
    url = f"https://www.zoodmall.uz/api/getproducts-list?deviceType=web&nocache=true&&rowsPerPage=48&categoryId=0&nameLike={encoded_query}&page=1&sort=1"
    headers = {
        "x-lang": "uz",
        "x-marketcode": "UZ" 
    }
    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        
    
        data = response.json()
        pprint(data['marketList'][0:5])
    else:
        print("İstek başarısız oldu. Durum kodu:", response.status_code)

        
def sello():

    response = requests.get(f"https://stg-api.sello.uz/algolia/search?query={encoded_query}&page=1&perPage=30")
    
    if response.status_code == 200:
        
    
        data = response.json()
        pprint(data['marketList'][0:5])
    else:
        print("İstek başarısız oldu. Durum kodu:", response.status_code)
