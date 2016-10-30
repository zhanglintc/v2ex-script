#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original scripts from: https://www.v2ex.com/t/303768

import re
import requests

requests.packages.urllib3.disable_warnings()

session = requests.Session()

v2ex_url = 'https://www.v2ex.com'
signin_url = v2ex_url + '/signin'
daily_url = v2ex_url + '/mission/daily'

username = 'username'
password = 'password'

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.71 Safari/537.36 OPR/35.0.2066.23 (Edition beta)',
    'Referer': signin_url,
}

session.headers = base_headers

resp = session.get(signin_url, verify = False)
u, p = re.findall(r'class="sl" name="([0-9A-Za-z]{64})"', resp.text)
once_code = re.search(r'value="(\d+)" name="once"', resp.text).group(1)

resp = session.post(signin_url, {u: username, p: password, 'once': once_code, 'next': '/'})
resp = session.get(daily_url)

if u'每日登录奖励已领取' in resp.text:
    print('Already got it.\n')

else:
    resp = session.get(v2ex_url + re.search(r'/mission/daily/redeem\?once=\d+', resp.text).group())
    print(resp.ok)


