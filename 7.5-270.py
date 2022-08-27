'''
完成工作：
  通过selenium便利列表页,获取每部电影的url
  获取每部电影的详情页
  提取每部电影的名称、类别、分数、简介、封面等内容
'''
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import urljoin
import logging
from os import makedirs
from os.path import exists
import json

url = r'https://spa2.scrape.center/'
index_url = r'https://spa2.scrape.center/page/{page}'
time_out = 10
total_page = 10
RESULT_DIR = 'result'

exists(RESULT_DIR) or makedirs(RESULT_DIR)
logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(levelname)s: %(message)s')

# 无头模式
options = webdriver.ChromeOptions()
options.add_argument('--headless')

browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, time_out)

def scrape_page(url, condition, locator):
  try:
    browser.get(url)
    wait.until(condition(locator))
  except:
    logging.error('error occurred while scraping %s', url, exc_info=True)

def scrape_index(page):
  url = index_url.format(page = page)
  scrape_page(url, condition=EC.visibility_of_all_elements_located, locator=(By.CSS_SELECTOR, '#index .item'))

def parse_index():
  elements = browser.find_elements(by=By.CSS_SELECTOR, value="#index .item .name")
  for element in elements:
    href = element.get_attribute('href')
    yield urljoin(index_url,href)

def scrape_detail(url):
  scrape_page(url, condition=EC.visibility_of_element_located, locator=(By.TAG_NAME, 'h2'))

def parse_detail():
  url = browser.current_url
  name = browser.find_element(By.TAG_NAME, 'h2').text
  categories = [element.text for element in browser.find_elements(By.CSS_SELECTOR, '.categories button span')]
  cover = browser.find_element(By.CSS_SELECTOR, '.cover').get_attribute('src')
  score = browser.find_element(By.CLASS_NAME, 'score').text
  drama = browser.find_element(By.CSS_SELECTOR, '.drama p').text

  return {
    'url':url,
    'name':name,
    'categories':categories,
    'cover':cover,
    'score':score,
    'drama':drama
  }

def save_data(data):
  name = data.get('name')
  data_path = f'{RESULT_DIR}/{name}.json'
  json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii = False, indent = 2)

def main():
  try:
    for page in range(1, total_page+1):
      scrape_index(page)
      detail_urls = parse_index()
      # logging.info('details urls %s', list(detail_urls))
      for detail_url in list(detail_urls):
        logging.info('get detail url %s', detail_url)
        scrape_detail(detail_url)
        detail_data = parse_detail()
        logging.info('detail data %s', detail_data)
        save_data(detail_data)
  finally:
    browser.close()

if __name__ == '__main__':
  main()