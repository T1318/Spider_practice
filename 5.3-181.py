from operator import le
import requests
import logging
import json


basic_url = r'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'
# logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s: %(messgae)s')

def scrape_api(url):
  # logging.info('scraping %s...', url)
  try:
    response = requests.get(url)
    if response.status_code == 200:
      return response.json()
  # else:
  #   return 0
    # logging.error('get invalid status code %s while scraping %s', response.status_code, url)
  except:
    # logging.error('error occurred while scraping %s', url, exc_info=True)
    None

LIMIT = 10

def scrape_index(page):
  url = basic_url.format(limit = LIMIT, offset = LIMIT*(page-1))
  return scrape_api(url)

detail_url = r'https://spa1.scrape.center/api/movie/{id}'

def scrape_detail(id):
  url = detail_url.format(id = id)
  return scrape_api(url)

TOTAL_page = 2

def main():
  for page in range(1, TOTAL_page + 1):
    index_data = scrape_index(page)
    for item in index_data.get('results'): # get为字典的函数，获取某个键的值
      id = item.get('id')
      detail_data = scrape_detail(id)
      # logging.info('detail data %s', detail_data)
      # print(detail_data)
      with open(file=r'F:\1-哈尔滨工业大学\Python爬虫\python3网络爬虫开发实战\5.3-181.txt', mode='a', encoding='utf-8') as f:
        f.write(json.dumps(detail_data, ensure_ascii=False))
        f.write('='*20)
if __name__ == '__main__':
  main()