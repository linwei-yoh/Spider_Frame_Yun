#!/usr/bin/env python4
# -*- coding: utf-8 -*-
# __author__ = 'AL'

import requests
import requests.adapters

from Mongo_Helper import MongoHelper
from Redis_Helper import RedisClient

from component.Spider import Spider as WebSpider
from component.Schedule import Schedule
from overwrite.Fetch_Worker import OwFetchWorker
from overwrite.Parse_Worker import OwPaeseWorker
from overwrite.Save_Worker import OwSaveWorker

from Config import config


def WebSpider_Start(start_tasks):
    # 持久化数据库
    mongo_client = MongoHelper()

    # 缓存数据库
    redis_client = RedisClient()
    redis_client.init_tables()

    thread_num = config.Spider_config.get("thread_num", 5)
    parser_num = config.Spider_config.get("parser_num", 1)
    max_retries = config.Spider_config.get("retry_times", 3)
    monitor_time = config.Spider_config.get("monitor_time", 5)
    start_time = config.Spider_config.get("fast_start", "20:00:00")
    end_time = config.Spider_config.get("fast_end", "6:00:00")
    fast_fcy = config.Spider_config.get("fast_fcy", 5)
    nor_fcy = config.Spider_config.get("nor_fcy", 5)
    fetch_interval = config.Spider_config.get("fetch_interval", 1)

    schedule = Schedule(start_time, end_time, fast_fcy, nor_fcy, fetch_interval)

    print("爬取开始:-----------------")
    with requests.Session() as session:
        session.mount('https://', requests.adapters.HTTPAdapter(pool_maxsize=thread_num))
        session.mount('http://', requests.adapters.HTTPAdapter(pool_maxsize=thread_num))

        # 配置组件
        fetch_worker = OwFetchWorker(session, max_repeat=max_retries)
        parse_worker = OwPaeseWorker()
        save_worker = OwSaveWorker(mongo_client)
        web_spider = WebSpider(fetch_worker, parse_worker, save_worker, schedule, redis_client)

        # 根据任务状态表 添加任务队列
        print("开始载入task:-----------------")
        p = redis_client.client.pipeline()
        for task in start_tasks:
            suburb, state, postcode = task
            redis_client.add_new_task(suburb, state, postcode, 1, "Rent")
            redis_client.add_new_task(suburb, state, postcode, 1, "Sold")
        p.execute()
        print("载入task完成:-----------------")

        # fetcher_num 采集线程数
        web_spider.start_work_and_wait_done(fetcher_num=thread_num, parser_num=parser_num, monitor_time=monitor_time)
    print("爬取完成")
    redis_client.init_tables()


if __name__ == '__main__':
    WebSpider_Start([])
