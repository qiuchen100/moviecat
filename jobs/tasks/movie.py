# -*- coding: utf-8 -*-#
import os, time, hashlib, json
import requests, re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from application import app, db
from common.libs.DateHelper import getCurrentTime
from common.models.moive import Movie


'''
python manager.py runjob -m movie
'''


class JobTask():

    def __init__(self):
        self.source = 'btbtdy'
        self.url = {
            'num': 3,
            'url': 'http://btbtdy1.com/btfl/dy1-{}.html',
            'path': '/Users/qiuchen/PycharmProjects/flask_base/tmp/{}/'.format(self.source)
        }

    def run(self, params):
        self.date = getCurrentTime('%Y%m%d')
        act = params['act']
        if act == 'list':
            self.getList()
        elif act == 'parse':
            self.parseInfo()

    def getList(self):
        '''
        获取列表
        '''
        config = self.url
        path_root = config['path'] + self.date
        path_list = path_root + '/list'
        path_info = path_root + '/info'
        path_json = path_root + '/json'
        path_vid = path_root + '/vid'
        self.makesureDirs(path_root)
        self.makesureDirs(path_list)
        self.makesureDirs(path_info)
        self.makesureDirs(path_json)
        self.makesureDirs(path_vid)
        pages = range(1, config['num'] + 1)
        for idx in pages:
            tmp_path = path_list + '/' + str(idx)
            tmp_url = config['url'].format(idx)
            if os.path.exists(tmp_path):
                continue
            app.logger.info('get list: {}'.format(tmp_url))
            tmp_content = self.getHttpContent(tmp_url)
            self.saveContents(tmp_path, tmp_content)
            time.sleep(0.5)

        for idx in os.listdir(path_list):
            tmp_content = self.getContent(path_list + '/' + str(idx))
            items_data = self.parseList(tmp_content)
            if not items_data:
                continue
            for item in items_data:
                tmp_json_path = path_json + '/' + item['hash']
                tmp_info_path = path_info + '/' + item['hash']
                tmp_vid_path = path_vid + '/' + item['hash']
                if not os.path.exists(tmp_json_path):
                    self.saveContents(tmp_json_path, json.dumps(item, ensure_ascii=False))
                if not os.path.exists(tmp_info_path):
                    tmp_content = self.getHttpContent(item['url'])
                    self.saveContents(tmp_info_path, tmp_content)
                if not os.path.exists(tmp_vid_path):
                    tmp_vid_url = item['url'].replace('/btdy/dy', '/vidlist/')
                    tmp_vid_content = self.getHttpContent(tmp_vid_url)
                    self.saveContents(tmp_vid_path, tmp_vid_content)



    def parseList(self, content):
        data = []
        config = self.url
        url_info = urlparse(config['url'])
        url_domain = url_info[0] + '://' + url_info[1]

        tmp_soup = BeautifulSoup(content, 'html.parser')
        tmp_list = tmp_soup.select('div.list_su ul li')
        for tmp_item in tmp_list:
            tmp_target = tmp_item.select('div a.pic_link')
            tmp_href = tmp_target[0]['href']
            tmp_name = tmp_target[0]['title']
            if not tmp_href.startswith('http://'):
                tmp_href = url_domain + tmp_href
            print(tmp_href + '  ' + tmp_name)
            tmp_data = {
                'name': tmp_name,
                'url': tmp_href,
                'hash': hashlib.md5(tmp_href.encode('utf-8')).hexdigest()
            }
            data.append(tmp_data)
        return data

    def parseInfo(self):
        '''
        解析详情信息
        '''
        config = self.url
        path_root = config['path'] + getCurrentTime('%Y%m%d')
        path_info = path_root + '/info'
        path_json = path_root + '/json'
        path_vid = path_root + '/vid'
        for filename in os.listdir(path_info):
            tmp_json_path = path_json + '/' + filename
            tmp_info_path = path_info + '/' + filename
            tmp_vid_path = path_vid + '/' + filename
            tmp_data = json.loads(self.getContent(tmp_json_path), encoding='utf-8')
            tmp_content = self.getContent(tmp_info_path)
            tmp_soup = BeautifulSoup(tmp_content, 'html.parser')
            tmp_vid_content = self.getContent(tmp_vid_path)
            tmp_vid_soup = BeautifulSoup(tmp_vid_content, 'html.parser')
            try:
                tmp_pub_date = tmp_soup.select('div.vod div.vod_intro dl dd')[0].getText()
                tmp_desc = tmp_soup.select('div.vod div.vod_intro div.des div.c05')[0].getText()
                tmp_classify = tmp_soup.select('div.vod div.vod_intro dl dd')[2].getText()
                tmp_actor = tmp_soup.select('div.vod div.vod_intro dl dd')[6].getText()
                tmp_pic_list = tmp_soup.select('div.vod div.vod_img img')
                tmp_pics = []
                for tmp_pic in tmp_pic_list:
                    tmp_pics.append(tmp_pic['src'])

                # 获取下载地址
                tmp_download_list = tmp_vid_soup.find_all('a', href=re.compile('magnet:?'))
                tmp_magnet_url = ''
                if tmp_download_list:
                    tmp_magnet_url = tmp_download_list[0]['href']

                tmp_data['pub_date'] = tmp_pub_date
                tmp_data['desc'] = tmp_desc
                tmp_data['classify'] = tmp_classify
                tmp_data['actor'] = tmp_actor
                tmp_data['magnet_url'] = tmp_magnet_url
                tmp_data['source'] = self.source
                tmp_data['created_time'] = tmp_data['updated_time'] = getCurrentTime()
                if tmp_pics:
                    tmp_data['cover_pic'] = tmp_pics[0]
                    tmp_data['pics'] = json.dumps(tmp_pics)

                tmp_movie_info = Movie.query.filter_by(hash = tmp_data['hash']).first()
                if tmp_movie_info:
                    continue
                tmp_model_movie = Movie(**tmp_data)
                db.session.add(tmp_model_movie)
                db.session.commit()
            except Exception as e:
                continue
        return True

    def getContent(self, path):
        if os.path.exists(path):
            with open(path) as f:
                return f.read()
        return ''

    def saveContents(self, path, content):
        if content:
            with open(path, mode='w+', encoding='utf-8') as f:
                if type(content) != str:
                    content = content.decode('utf-8')
                f.write(content)
                f.flush()

    def makesureDirs(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def getHttpContent(self, url):
        try:
            headers = {
                'Content-Type': 'text/html;charset=utf-8',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                'Referer': "http://btbtdy1.com/btdy/dy18196.html",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
            }
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                app.logger.info(r.status_code)
                return None
            return r.content
        except Exception:
            return None
