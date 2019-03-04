# -*- coding: utf-8 -*-
import os
import pymongo
import smtplib
from scrapy.conf import settings
from scrapy.mail import MailSender
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from os.path import join, dirname
from dotenv import load_dotenv
# from scrapy import log

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JobsPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '.env'))
    load_dotenv(dotenv_path)
    collection_name = 'OnlineJobsCollection'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DB'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        if spider.name == 'weld_county_spider':
            return
        spider_name = spider.name
        subject = "Crawl Completed for %s" % spider_name
        self.send_mail("Crawl completed.", subject)
        self.client.close()

    def process_item(self, item, spider):
        # Check if description_url matches any other record in the DB
        if spider.name == 'weld_county_spider':
            return item

        item_dict = dict(item)
        db_record = self.db[self.collection_name].find_one({ 'description_url': item_dict['description_url'] })
        # If there's a match, update is_new_job field to 0
        if db_record == None:
            item_dict['is_new_job'] = 1
            self.db[self.collection_name].insert_one(item_dict)
        # If there's NO match, insert the record with the is_new_job field set to 1
        else:
            self.db[self.collection_name].update_one({ 'description_url': item_dict['description_url'] }, {'$set': { 'is_new_job': 0 }})
     
        return item
    
    def send_mail(self, message, title):
        gmailUser = os.getenv('SMTP_USER')
        gmailPassword = os.getenv('SMTP_PASS')
        recipient = os.getenv('MAIL_TO')
        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = recipient
        msg['Subject'] = title
        msg.attach(MIMEText(message))

        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipient, msg.as_string())
        mailServer.close()