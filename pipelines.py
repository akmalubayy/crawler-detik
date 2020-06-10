	# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging, sys
import json
import psycopg2
from crawl.spiders.postgredb import connectDbAndQuery
from crawl.spiders.config import config


# config module
logging.basicConfig(filename='example.log',level=logging.DEBUG)

class DetikPipeline(object):

    # read connection parameters
    params = config()
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    # set autocommit 
    conn.autocommit = True

    def open_spider(self, spider):
        self.file = open('pipeline.log', 'w')
        self.register_urls = []

    def close_spider(self, spider):
        self.file.close()

    def query_search(self,search_href):
        conn = None
        result = 0
        try :
            # create a cursor
            cur = self.conn.cursor()
            # execute a statement
            query = "SELECT COUNT(*) FROM  scr_raw_content WHERE url = '"+search_href+"'"
            cur.execute(query)
            print(search_href)
            (result,)=cur.fetchone()
            # close connection
            cur.close()
        except Exception as e:
          logging.debug(str(e))

        return result

    def process_item(self, item, spider):
        # try :
	       #  line = json.dumps(dict(item))
	       #  self.file.write(json.loads(line))
        # except Exception as e:
        #     logging.debug(str(e))

        # save data into database
        conn = None
        try:
            # filter by url & kick if duplicate
            if(item["url"] in self.register_urls):
                return None
            else :
                # append new url to stack 
                self.register_urls.append(item["url"])
                rc = self.query_search(item["url"])
                if rc < 1 :
                    # create a cursor
                    cur = self.conn.cursor()
                    # execute a statement
                    query = "INSERT INTO scr_raw_content (title,date,content,url,ctime,crawl_agent) VALUES (%s,%s, %s, %s, NOW(), %s)"
                    data = (item["title"],item["datetime"], item["content"], item["url"],1)
                    cur.execute(query, data)
                    # close connection
                    cur.close()
        except Exception as e:
          logging.debug(str(e))

        return item