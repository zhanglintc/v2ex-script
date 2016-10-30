#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original scripts from: https://www.v2ex.com/t/315502

from bs4 import BeautifulSoup
import requests
import requests.packages.urllib3
import time
import random

requests.packages.urllib3.disable_warnings() # disable warning by zhanglintc

username = 'username'
password = 'password'

loginUrl = 'https://www.v2ex.com/signin'
activityUrl = 'https://www.v2ex.com/'
fresh_times = 2
sleep_time = 1.5

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'upgrade-insecure-requests': 1,
    'referer': loginUrl,
}

session = requests.Session()

loginRes = session.get(loginUrl, headers = headers, verify = False) # add verify = False by zhanglintc

soup = BeautifulSoup(loginRes.text, 'html.parser')
params = {
    soup.find_all('input', {'class': 'sl'})[0].attrs['name']: username,
    soup.find_all('input', {'class': 'sl'})[1].attrs['name']: password,
    'once': soup.find('input', {'name': 'once'}).attrs['value'],
    'next': '/',
}

session.post(loginUrl, params, headers = headers)

for i in range(fresh_times):
    session.get(activityUrl, headers = headers)
    time.sleep(sleep_time)

    print '{0}/{1}'.format(i + 1, fresh_times)


