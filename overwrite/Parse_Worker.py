#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from component.Parse_Thread import ParseWorker

from parser_to_dir import parse_detail


class OwPaeseWorker(ParseWorker):
    def html_parse(self, params, content):
        try:
            parse_result, url_list, save_list = self.working(params, content)
        except Exception as excep:
            parse_result, url_list, save_list = -1, [], []

        if 0 < self.max_deep <= params["Deep"]:
            url_list = []
        return parse_result, url_list, save_list

    def working(self, params, content):
        result, url_list, save_list = parse_detail(params, content)
        if result == -1:
            return -1, [], []
        else:
            return 1, url_list, save_list


if __name__ == '__main__':
    pass
