#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from Mongo_Helper import MongoHelper
from SpiderRun import WebSpider_Start
import pickle


if __name__ == '__main__':
    with open("suburb.pkl", 'rb') as f:
        suburb_items = pickle.load(f)

    # 开始爬取
    WebSpider_Start(suburb_items)
