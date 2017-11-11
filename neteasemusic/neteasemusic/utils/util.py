#coding = utf-8
from Crypto.Cipher import AES
import base64
import requests
import json

# from bs4 import BeautifulSoup
# import requests
# import random

# headers = {
#     'Cookie': 'appver=1.5.0.75771;',
#     'Referer': 'http://music.163.com/'
# }

music_domain_url = "http://music.163.com/weapi/song/enhance/player/url?csrf_token="
second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"

# url = 'http://www.xicidaili.com/nn/'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
# }

# def get_ip_list(url, headers):
#     web_data = requests.get(url, headers=headers)
#     soup = BeautifulSoup(web_data.text, 'lxml')
#     ips = soup.find_all('tr')
#     ip_list = []
#     for i in range(1, len(ips)):
#         ip_info = ips[i]
#         tds = ip_info.find_all('td')
#         ip_list.append(tds[1].text + ':' + tds[2].text)
#     return ip_list

# ip_list = get_ip_list(url, headers=headers)

def get_params(id):
    first_param = "{\"ids\":\"["+str(id)+"]\",\"br\":128000,\"csrf_token\":\"\"}"
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey
    

def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


def get_json(url, params, encSecKey):
    data = {
         "params": params,
         "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content

def get_music_url(id):
    params = get_params(id);
    encSecKey = get_encSecKey();
    
    json_text = get_json(music_domain_url, params, encSecKey)
    json_dict = json.loads(json_text)
    if json_dict['code'] == 200:
        return json_dict['data'][0]['url']
    return None



# def get_random_ip(ip_list):
#     proxy_list = []
#     for ip in ip_list:
#         proxy_list.append('http://' + ip)
#     proxy_ip = random.choice(proxy_list)
#     proxies = {'http': proxy_ip}
#     return proxies


if __name__ == "__main__":
    #print get_music_url(365755)

    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    proxies = get_random_ip(ip_list)
    print(proxies)