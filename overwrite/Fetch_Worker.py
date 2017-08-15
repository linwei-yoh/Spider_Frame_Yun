#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

import requests
from utilities import make_random_useragent
from component.Fetch_Thread import FetchWorker
from Config import config


class OwFetchWorker(FetchWorker):
    def __init__(self, session, max_repeat, cloud=False):
        FetchWorker.__init__(self, max_repeat)
        self.session = session
        self.cloud = cloud

    def url_fetch(self, params):
        try:
            fetch_result, content = self.working(params)
        except Exception:
            repeat = params["Repeat"]
            if repeat >= self.max_repeat:
                fetch_result, content = -1, None
            else:
                fetch_result, content = 0, None

        return fetch_result, content

    @staticmethod
    def get_url(params):
        url_header = {"User-Agent": make_random_useragent()}
        url_params = None

        src_type = params["Keys"][0]
        if src_type == "property":
            address = params["Keys"][1]
            tar_url = "https://www.asd.com.au/property/" + address
        elif src_type == "history":
            tar_url = None
        elif src_type == "school":
            tar_url = None
        else:
            tar_url = None
        return tar_url, url_header, url_params

    @staticmethod
    def get_proxy_abuyun():
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": config.abuyun_config['proxyHost'],
            "port": config.abuyun_config['proxyPort'],
            "user": config.abuyun_config['proxyUser'],
            "pass": config.abuyun_config['proxyPass'],
        }

        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        return proxies

    def working(self, params):

        tar_url, url_header, url_params = self.get_url(params)

        if self.cloud:
            proxies = self.get_proxy_abuyun()
            timeout = (9.05, 20)
        else:
            proxies = None
            timeout = (6.05, 20)

        r = requests.get(tar_url, headers=url_header, params=url_params, proxies=proxies, timeout=timeout,
                         allow_redirects=False)
        result = r.text

        if r.status_code == 200:
            return 1, result
        else:
            r.raise_for_status()


if __name__ == '__main__':
    pass
