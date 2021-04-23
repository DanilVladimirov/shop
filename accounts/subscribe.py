from shop.settings import SITE_URL
from accounts.models import *
from product.models import *
import requests
import json
from dotenv import load_dotenv
load_dotenv()
import os


TG_TOKEN = os.environ.get('TG_TOKEN')


def geo_ip_info(ip_address):
    req = requests.get(f'http://ipwhois.app/json/{ip_address}').json()
    response = {}
    if req.get('success'):
        response['country'] = req.get('country') if req.get('country') else ''
        response['region'] = req.get('region') if req.get('region') else ''
        response['city'] = req.get('city') if req.get('city') else ''
    return response


def subscribe_answer_support(id_user, text_answer):
    pass
    

def subscribe_create_order(id_user, id_order, url_order):
    pass

def subscribe_authorization(id_user, session_key, ip):
    pass


def subscribe_promo(text_msg):
    pass

    
def subscribe_get_file_in_order(id_user, id_order):
    pass
    

def subscribe_edit_price(lst, name, new_price):
    pass