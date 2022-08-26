import logging
from time import time
import requests
import re
from urllib.parse import urljoin

import json
from os import makedirs
from os.path import exists

import multiprocessing

logging.basicConfig(level = logging.INFO, format='%(asctime)s-%(levelname)s:%(message)s')
url_basic = 'https://ssr1.scrape.center'
total_page = 10

# 获取网页源代码
def get_url(url):
  logging.info('scraping %s', url)
  try:
      response = requests.get(url)
      if response.status_code == 200:
        return response.text
      logging.error('get invalid status code %s while scraping %s', response.status_code, url)
  except:
      logging.error('error occurred while scraping %s', url, exc_info = True)

# 组合成爬取n页的主页网址
def scrape_index(page):
  index_url = f'{url_basic}/page/{page}'
  return get_url(index_url)

# 获取每个电影页面的网址
def parse_index(html):
  pat = re.compile(r'<a.+?href="(.+?)" class="name">')
  items = re.findall(pat, html)
  if not items:
    return []
  for item in items:
    detail_url = urljoin(url_basic, item)
    logging.info('get detail url %s', detail_url)
    yield detail_url
  
# 返回处理后的网页源代码
def scrape_detail(url):
  return get_url(url)

# 获取电影页面信息
def parse_detail(html):
  cover_pat = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
  name_pat = re.compile('<h2.*?>(.+?)</h2>')
  class_pat = re.compile('<button.*?category.*?<span>(.+?)</span>.*?</button>', re.S)
  score_pat = re.compile('<p.+?class="score.+?">(.+?)</p>', re.S)
  drama_pat = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
  time_pat = re.compile('(\d{4}-\d{2}-\d{2})\s?上映', re.S)

  cover = re.search(cover_pat, html).group(1).strip() if re.search(cover_pat, html) else None
  name = re.search(name_pat, html).group(1).strip() if re.search(name_pat, html) else None
  class_name = re.findall(class_pat, html) if re.search(class_pat, html) else []
  score = float(re.search(score_pat, html).group(1).strip()) if re.search(score_pat, html) else None
  drama = re.search(drama_pat, html).group(1).strip() if re.search(drama_pat, html) else None
  time = re.search(time_pat, html).group(1).strip() if re.search(time_pat, html) else None

  return {
    'cover':cover,# 封面
    'name':name,# 名称
    'categories':class_name,# 分类名
    'published_at':time,# 发布时间
    'drama':drama,# 简介
    'score':score# 评分
  }

RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

def save_data(data):
  name = data.get('name')
  data_path = f'{RESULTS_DIR}/{name}.json'
  json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# 主函数
def main(page):
  
  index_html = scrape_index(page)
  detail_urls = parse_index(index_html)
  for detail_url in detail_urls:
    detail_html = scrape_detail(detail_url)
    data = parse_detail(detail_html)
    logging.info('get detail data %s', data)
    save_data(data)


if __name__ == '__main__':
  pool = multiprocessing.Pool()
  pages = range(1, total_page+1)
  pool.map(main, pages)
  pool.close()
  pool.join()

