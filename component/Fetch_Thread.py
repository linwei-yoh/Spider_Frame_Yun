#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import queue

from Spider_Manager import ThreadSta
from logger_config import report_logger
from functools import partial
import traceback


class FetchWorker(object):
    """
    覆盖url_fetch方法
    """

    def __init__(self, max_repeat):
        self.max_repeat = max_repeat

    def url_fetch(self, params):
        result = params
        return result


class FetchThread(Thread):
    def __init__(self, client, worker, num, spiderManager):
        """
        建立爬取线程
        :param worker: 爬取处理类
        :param num: 爬取线程最大数量
        :param spiderManager: 爬虫管理

        """
        Thread.__init__(self, name='Fetcher')
        self.client = client
        self.worker = worker
        self.num = num
        self.spiderManager = spiderManager

    def run(self):
        self.spiderManager.Fetch_Sta = ThreadSta.Work
        try:
            self._run()
        except Exception as exc:
            report_logger.error("FetchThread :\n" + traceback.format_exc())
            self.spiderManager.Fetch_Sta = ThreadSta.Error

    def _run(self):
        with ThreadPoolExecutor(max_workers=self.num) as executor:
            while True:
                try:
                    params = self.spiderManager.fetch_queue.get(block=True, timeout=5)
                    executor.submit(self.worker.url_fetch, params) \
                        .add_done_callback(partial(self.callback, params))
                except queue.Empty:
                    if self.spiderManager.Fetch_Sta == ThreadSta.Finish:
                        break

    def callback(self, params, value):
        fetch_result, content = value.result()

        # 爬取成功
        if fetch_result > 0:
            self.spiderManager.parse_queue.put_nowait([params, content])
        # 重新爬取
        elif fetch_result == 0:
            params["Repeat"] += 1
            self.spiderManager.fetch_queue.put_nowait(params)
        # 爬取失败
        elif fetch_result == -1:
            deep = params["Deep"]
            repeat = params["Repeat"]
            # self.client.add_idle_task(suburb, state, index, deep, repeat)
        # 致命性失败
        elif fetch_result == -2:
            self.spiderManager.save_queue.put_nowait([params, False])

        self.spiderManager.fetch_queue.task_done()  # 可能因为线程池报错而没执行到


if __name__ == '__main__':
    pass
