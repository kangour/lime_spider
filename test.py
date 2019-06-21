import logging
from lime_spider import Store, ApiClient, UrlClient, SeleniumClient, Runner
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    #  #  将 json 存到电子表格
    #  lists = [
    #      dict(a=1, b=2, c=3),
    #      dict(a=11, b=12, c=13),
    #      dict(a=21, b=22, c=23),
    #  ]
    #  store = Store(filename='result', suffix='xlsx', path='./')
    #  store.save_to_xls(lists)
    #  logger.info('Success')

    #  #  文件下载
    #  homepage = 'http://npm.taobao.org/mirrors/chromedriver/2.23/chromedriver_linux64.zip'
    #  store = Store(filename='chromedriver_linux64', suffix='zip', path='./')
    #  store.download(homepage)

    #  #  文本保存
    #  store = Store(filename='文本文档', suffix='txt', path='./')
    #  store.writer('hello world！')

    #  #  ApiClient 爬取 unsplash 网站的高清图片下载链接
    #  homepage = 'https://unsplash.com/napi/photos?page=1&per_page=30'
    #  client = ApiClient(homepage)
    #  for i in client.data:
    #      logger.info('{0}'.format(i['urls']['raw']))

    #  使用 Runner 多进程下载 unsplash 网站的高清图片
    homepage = 'https://unsplash.com/napi/photos?page=1&per_page=30'
    client = ApiClient(homepage)
    runner = Runner()
    for i in client.data:
        filename = i['id']
        url = i['urls']['raw']
        store = Store(filename=filename, suffix='jpg', path='./')
        logger.info('{0}'.format(i['urls']['raw']))
        runner.start(store.download, url)
    runner.end()

    #  #  UrlClient 爬取起点小说的免费小说链接
    #  homepage = 'https://www.qidian.com/free'
    #  client = UrlClient(homepage)
    #  element = client.find('div', {'class': 'book-img-text'})
    #  element = client.find_all_sub(element, 'li')
    #  for i in element:
    #      i = client.find_sub(i, 'a', {'data-eid': 'qd_E05'})
    #      logger.info(i['href'])

    #  #  SeleniumClient 爬取安居客的小区信息
    #  homepage = 'https://shaoxing.anjuke.com/community/p1'
    #  # client = SeleniumClient(homepage, 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    #  client = SeleniumClient(homepage, '/root/chromedriver')
    #  element = client.find_all('div', {'class': 'li-itemmod'})
    #  logger.info(element)

    #  #  实战 1：爬安居客小区信息
    #  import re
    #  homepage = 'https://shaoxing.anjuke.com/community/p{}/'
    #  for i in range(1):
    #      logger.info('第 %s 页' % str(i + 1))
    #      url = homepage.format(i + 1)
    #      client = SeleniumClient(url, 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    #      # client = SeleniumClient(url, '/root/chromedriver')
    #      element = client.find_all('div', {'class': 'li-itemmod'})
    #      dic = {}
    #      _list = []
    #      for community in element:
    #          list_info = client.find_sub(community, 'div', {'class', 'li-info'})
    #          name = list_info.h3.a.text.strip()
    #          _list.append(dict(
    #              name=name,
    #              url=list_info.h3.a['href'].strip(),
    #              date=client.find_sub(list_info, 'p', {'class', 'date'}).text.strip(),
    #              district=re.split('［|］|-', list_info.address.text.strip())[1],
    #              square=re.split('［|］|-', list_info.address.text.strip())[2],
    #              street=re.split('［|］|-', list_info.address.text.strip())[3],
    #          )
    #          )
    #          logger.info(name)
