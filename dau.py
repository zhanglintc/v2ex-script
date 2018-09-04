#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original scripts from: https://www.v2ex.com/t/315502

from bs4 import BeautifulSoup
import requests
import requests.packages.urllib3
import time, re
import random
import pdb

requests.packages.urllib3.disable_warnings() # disable warning by zhanglintc

loginUrl = 'https://www.v2ex.com/signin'
activityUrl = 'https://www.v2ex.com/'

fresh_times = 1000
sleep_time = 3

username = 'username'
password = 'password'

cookie_file = "cookie.txt"

def recognize_captcha(session, response):
    mc = re.search("_captcha\?once=\d+", response.text)

    if mc:
        captcha = mc.group()
        captcha_url = "https://www.v2ex.com/{0}".format(captcha)
        pic = session.get(captcha_url)

        fw = open("captcha.png", "wb")
        fw.write(pic.content)
        fw.close()

    # TODO: send to wechat and wait response
    wx_reponse = "wx_reponse"
    # wx_reponse = raw_input("enter capcha: ")
    requests.get("http://ali.zhanglintc.work:8000/send?text=v2ex_dau_cookie_out_of_date")

    return wx_reponse

def update_cookies():
    for i in range(3):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'upgrade-insecure-requests': 1,
            'referer': loginUrl,
        }

        session = requests.Session()
        response = session.get(loginUrl, headers=headers, verify=True)

        captcha = recognize_captcha(session, response)

        soup = BeautifulSoup(response.text, 'html.parser')
        params = {
            soup.find_all('input', {'class': 'sl'})[0].attrs['name']: username,
            soup.find_all('input', {'class': 'sl'})[1].attrs['name']: password,
            soup.find_all('input', {'class': 'sl'})[2].attrs['name']: captcha,
            'once': soup.find('input', {'name': 'once'}).attrs['value'],
            'next': '/',
        }

        post_response = session.post(loginUrl, params, headers=headers)

        if "/member/zhanglintc" in post_response.text:
            break

    set_cookie = post_response.history[0].headers['set-cookie']

    fw = open(cookie_file, "wb")
    fw.write(set_cookie)
    fw.close()

    session.close()

def get_cookie():
    cookie = ""

    try:
        fr = open(cookie_file, "rb")
        cookie = fr.read()
        fr.close()
    except:
        pass

    return cookie

def check_cookie():
    cookie = get_cookie()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'upgrade-insecure-requests': 1,
        'referer': activityUrl,
        'cookie': cookie,
    }

    session = requests.Session()
    html = session.get(activityUrl, headers=headers)

    if "/member/zhanglintc" in html.text:
        return True
    else:
        return False

def refresh():
    cookie = get_cookie()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'upgrade-insecure-requests': 1,
        'referer': activityUrl,
        'cookie': cookie,
    }

    session = requests.Session()
    for i in range(fresh_times):
        print '{0}/{1}'.format(i + 1, fresh_times)

        b = session.get(activityUrl, headers=headers)
        time.sleep(sleep_time)

    session.close()

def main():
    if not check_cookie():
        update_cookies()

    refresh()

if __name__ == '__main__':
    main()

