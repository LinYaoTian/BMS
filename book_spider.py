# -*- coding: UTF-8 -*-
# encoding: utf-8
import sys
import time
from urllib import request
import mysql.connector
import importlib
import random
from bs4 import BeautifulSoup
import logging
from logging.handlers import TimedRotatingFileHandler

importlib.reload(sys)


########## Configure logging #############
logFilePath = "log/spider/book_spider.log"
logger = logging.getLogger("Spider")
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler(logFilePath,
                                   when="D",
                                   interval=1,
                                   backupCount=30,
                                   encoding='utf-8'
                                   )
formatter = logging.Formatter('%(asctime)s \
%(filename)s[line:%(lineno)d] %(levelname)s %(message)s', )
handler.suffix = "%Y%m%d"
handler.setFormatter(formatter)
logger.addHandler(handler)

# Some User Agents
hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
       {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]


def book_spider():
    # 起始页数
    page_num = 0
    # 连接数据库
    conn = mysql.connector.connect(
        user='root',
        password='25283282',
        db='bms',
        use_unicode=True, )
    cur = conn.cursor(buffered=True)
    while (1):
        # 爬取的页面
        url = 'https://www.douban.com/tag/%E6%97%B6%E5%B0%9A/book?start=0' + str(page_num * 15)
        time.sleep(random.randint(0, 1))
        # Last Version
        # 爬虫的基本操作
        try:
            req = request.urlopen(url)
            source_code = req.read()
            plain_text = str(source_code, 'utf-8')
        except BaseException as e:
            print("book_spider error：" + str(e))
            logger.debug("book_spider error：" + str(e))
            return

        # debug_url = 'https://book.douban.com/subject/30301376/?from=tag_all'
        # debug = True
        try:
            soup = BeautifulSoup(plain_text)
            list_soup = soup.find('div', {'class': 'mod book-list'})
            for book_info in list_soup.findAll('dd'):
                book_url = book_info.find('a', {'class': 'title'}).get('href')
                # if debug:
                #     if book_url == debug_url:
                #         debug = False
                #     else:
                #         # 跳过
                #         continue
                book_msg = get_book_msg(book_url)
                if book_msg == ():
                    # 页面不存在 404
                    continue
                else:
                    # 判断是否有重复
                    cur.execute('SELECT * FROM book where isbn = %s', (book_msg['isbn'],))
                    conn.commit()
                    if cur.fetchone():
                        # 已经存在这本书
                        print("已存在：" + book_msg['name'])
                        logger.debug("已存在：" + book_msg['name'])
                        continue
                    else:
                        print("存储数据库：" + book_msg['name'])
                        logger.debug("存储数据库：" + book_msg['name'])
                        cur.execute(
                            'insert into book(name,isbn,location,state,author,publishingHouse,coverUrl,intro)values(%s,%s,%s,%s,%s,%s,%s,%s)',
                            (
                                book_msg['name'],
                                book_msg['isbn'],
                                book_msg['location'],
                                book_msg['state'],
                                book_msg['author'],
                                book_msg['publishingHouse'],
                                book_msg['coverUrl'],
                                book_msg['intro'])
                        )
                        conn.commit()
            page_num += 1
            # 最终爬的页数
            if page_num == 50:
                print("爬虫正常结束!")
                break
        except BaseException as e:
            print("发生错误！" + str(e) + "\n" + 'currentPage=' + str(page_num) + '\n' + 'error bookName:' + book_msg[
                'name'] + "\nbook_url=" + book_url)
            logger.debug(
                "发生错误！" + str(e) + "\n" + 'currentPage=' + str(page_num) + '\n' + 'error bookName:' + book_msg[
                    'name'] + "\nbook_url=" + book_url)
            return


def get_book_msg(url):
    try:
        req = request.urlopen(url)
        source_code = req.read()
        plain_text = str(source_code, 'utf-8')
        soup = BeautifulSoup(plain_text)
        isnb = ''
        author = soup.find('div', {'id': 'info'}).find('a').get_text().replace(' ', '')
        publishingHouse = ''
        for x in soup.find('div', {'id': 'info'}).findAll('span'):
            if x.get_text() == 'ISBN:':
                isnb = (''.join(x.nextSibling)).strip()
            elif x.get_text() == '出版社:':
                publishingHouse = (''.join(x.nextSibling)).strip()
        coverUrl = soup.find('a', {'class': 'nbg'}).find('img').get('src')
        count = 0
        intro = ''
        for x in soup.find('div', {'class': 'intro'}).findAll('p'):
            intro += '\t' + x.get_text()
            count += 1
            if count >= 2:
                break
            intro += '\n'
        location = str(random.randint(1, 99)) + '排' + str(random.randint(1, 50)) + '架'
        name = soup.find('div', {'id': 'wrapper'}).find('span', {'property': 'v:itemreviewed'}).get_text()
        return {
            'isbn': isnb,
            'coverUrl': coverUrl,
            'intro': intro,
            'state': 0,
            'location': location,
            'author': author,
            'name': name,
            'publishingHouse': publishingHouse}
    except BaseException as e:
        print('get_book_msg error:' + str(e))
        logger.debug('get_book_msg error:' + str(e)+',bookUrl='+url)
        return ()


if __name__ == '__main__':
    book_spider()
