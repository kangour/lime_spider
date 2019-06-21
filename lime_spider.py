import os
import sys
import time
import json
import urllib
import requests
from openpyxl import Workbook
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

'''
描述：lime spider 爬虫框架，支持爬 api、普通 url，可驱动浏览器
作者：kangour
邮箱：kangour@sina.cn
日期：2019年6月20日
更新：
使用：
    ApiClient 传入 url，method 和 params 爬 api，返回值是 json
    UrlCLient 掺入 url 爬页面，返回值是 html
    SeleniumClient 传入 url 和 webdriver 用浏览器爬页面，返回值是 html
    Store 文件存储

'''


class Base:

    def __init__(self):
        self._http = requests.Session()

    def request(self, method, url, **kwargs):
        res = self._http.request(
            method=method,
            url=url,
            **kwargs
        )
        return res

    def get(self, url, **kwargs):
        return self.request(
            method='GET',
            url=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self.request(
            method='POST',
            url_or_endpoint=url,
            **kwargs
        )


class Parser:

    def __init__(self):
        self.soup = BeautifulSoup(self.data, 'lxml')

    @property
    def data(self):
        raise NotImplementedError

    def find(self, tag, attrs={}):
        return self.soup.find(name=tag, attrs=attrs)

    def find_all(self, tag, attrs={}):
        return self.soup.find_all(name=tag, attrs=attrs)

    @staticmethod
    def find_sub(soup, tag, attrs={}):
        return soup.find(name=tag, attrs=attrs)

    @staticmethod
    def find_all_sub(soup, tag, attrs={}):
        return soup.find_all(name=tag, attrs=attrs)


class Store:

    def __init__(self, filename='result', suffix=None, path='./'):
        self.filename = filename
        self.suffix = suffix
        self.path = path
        self.file = filename + '.' + suffix
        self.fullname = path + filename + '.' + suffix
        self.check_file()

    def check_file(self):
        '''
        清理同名文件
        '''
        logger.info('file list %s' % os.listdir(self.path))
        logger.info('target file %s' % self.file)
        if self.file in os.listdir(self.path) and os.path.isfile(self.file):
            os.remove(os.path.join(self.path, self.file))

    def writer(self, *content):
        '''
        将文本写入文件
        :param content:
        :return:
        '''
        with open(self.fullname, 'a') as f:
            for i in content:
                f.write(i)
                f.write('\n\n')

    @staticmethod
    def reporthook(done_block, block_size, file_size):
        progress = min(int(done_block * block_size / file_size * 100), 100)
        sys.stdout.write('\r|{}{}| {}% {:.2f}M / {:.2f}M'.format(progress * '▇', (100 - progress) * ' ', progress,
                                                                 done_block * block_size / 1024 / 1024,
                                                                 file_size / 1024 / 1024))

    def download(self, url):
        '''
        根据 url 下载文件
        :param url:
        :return:
        '''
        urllib.request.urlretrieve(url, self.fullname, self.reporthook)
        sys.stdout.write('\n')
        logger.info('{} download complete!'.format(self.file))

    def save_to_xls(self, lists):
        '''
        将 json 格式的字典列表存入表格，支持自动存表头
        :param lists: 举例 [dict(a=1, b=2), dict(a=1, b=2)]
        :return:
        '''
        wb = Workbook()
        ws = wb.active
        ws.title = self.filename
        ws.append(list(lists[0].keys()))
        for dic in lists:
            ws.append(list(dic.values()))
        wb.save(self.fullname)


class ApiClient(Base):

    def __init__(self, url, method='GET', params=None):
        self.url = url
        self.method = method
        self.params = params
        super().__init__()

    @property
    def data(self):
        if self.method.upper() == 'GET':
            res = self.get(url=self.url, params=self.params)
        elif self.method.upper() == 'POST':
            res = self.post(url=self.url, data=self.params)
        else:
            raise TypeError('request method error')

        return json.loads(res.text)


class UrlClient(Base, Parser):

    def __init__(self, url):
        self.url = url
        super().__init__()
        super(Base, self).__init__()

    @property
    def data(self):
        res = self.get(url=self.url)
        return res.text


class SeleniumClient(Parser):

    def __init__(self, url, chrome_driver):
        self.url = url
        self.chrome_driver = chrome_driver
        super().__init__()

    @property
    def data(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        browser = webdriver.Chrome(executable_path=self.chrome_driver, chrome_options=options)
        browser.get(self.url)
        time.sleep(2)
        js = 'window.scrollBy(0,3000)'
        browser.execute_script(js)
        js = 'window.scrollBy(0,5000)'
        browser.execute_script(js)
        html = browser.page_source
        return html
