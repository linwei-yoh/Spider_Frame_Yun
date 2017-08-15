#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : AL

import re
from pyquery import PyQuery as pq
from component.logger_config import report_logger
import traceback


def parse_detail(params,content):
    try:
        doc = pq(content)
        task_list = list()
        save_list = list()
        return task_list, save_list
    except Exception as excep:
        report_logger.error("\n" + params + "\n" + traceback.format_exc())
        raise excep


if __name__ == '__main__':
    pass
