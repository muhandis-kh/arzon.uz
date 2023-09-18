import os
from dotenv import load_dotenv

load_dotenv()

zoodmall_api_link = os.getenv('zoodmall_api_link')
sello_api_link = os.getenv('sello_api_link')
olcha_api_link = os.getenv('olcha_api_link')
texnomart_api_link = os.getenv('texnomart_api_link')

korrektor_token = os.getenv('korrektor_token')

bot_token = os.getenv('bot_token')
secret_key = os.getenv('secret_key')