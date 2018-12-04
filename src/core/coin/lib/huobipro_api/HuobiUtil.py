# -*- coding: utf-8 -*-

import base64
import datetime
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request

import requests

# API 请求地址
API_URL = "https://api.huobi.pro"

# timeout in 10 seconds:
TIMEOUT = 10


def http_get_request(url, params, add_to_headers=None, proxies=None):
    headers = {
        "Content-type":
        "application/x-www-form-urlencoded",
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)
    try:
        response = requests.get(
            url, postdata, headers=headers, proxies=proxies, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                "request response status failed, status=%s" % response.status_code)
    except BaseException as e:
        raise Exception("httpGet failed, detail is: err=%s" % e)


def http_post_request(url, params, add_to_headers=None, proxies=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params)
    try:
        response = requests.post(
            url, postdata, headers=headers, proxies=proxies, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                "request response status failed, status=%s" % response.status_code)
    except BaseException as e:
        raise Exception("httpPost failed, detail is: err=%s" % e)


def api_key_get(params, request_path, ACCESS_KEY, SECRET_KEY, proxies=None):
    method = 'GET'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params.update({
        'AccessKeyId': ACCESS_KEY,
        'SignatureMethod': 'HmacSHA256',
        'SignatureVersion': '2',
        'Timestamp': timestamp
    })

    host_url = API_URL
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params['Signature'] = createSign(params, method, host_name, request_path,
                                     SECRET_KEY)

    url = host_url + request_path
    return http_get_request(url, params, add_to_headers=None, proxies=proxies)


def api_key_post(params, request_path, ACCESS_KEY, SECRET_KEY, proxies=None):
    method = 'POST'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params_to_sign = {
        'AccessKeyId': ACCESS_KEY,
        'SignatureMethod': 'HmacSHA256',
        'SignatureVersion': '2',
        'Timestamp': timestamp
    }

    host_url = API_URL
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params_to_sign['Signature'] = createSign(params_to_sign, method, host_name,
                                             request_path, SECRET_KEY)
    url = host_url + request_path + '?' + urllib.parse.urlencode(
        params_to_sign)
    return http_post_request(url, params, add_to_headers=None, proxies=proxies)


def createSign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')

    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature
