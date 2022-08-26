import re

import requests


def get_url(url, headers):
    r = requests.get(url, headers=headers)
    return r.text


def get_title(html):
    pat = r'<h2.*?class="m-b-sm">(.*?)</h2>'
    result = re.search(pat, html, re.S)
    return result


def get_image(html):
    pat = r'<img.*?src="(.*?)" class="cover">'
    result = re.search(pat, html, re.S)
    return result


def get_class(html):
    pat = r'<div.+?class="categories">.+?<span>(.+?)</span>.+?<span>(.+?)</span>'
    result = re.search(pat, html, re.S)
    return result


if __name__ == '__main__':
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    for i in range(10):
        url = r'https://ssr1.scrape.center/detail/' + str(i+1)
        html = get_url(url, headers)
        title = get_title(html)
        img = get_image(html)
        cls = get_class(html)
