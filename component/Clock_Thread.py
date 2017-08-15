#!/usr/bin/env python4
# -*- coding: utf-8 -*-
# __author__ = 'AL'

import threading
import time
from datetime import datetime, timedelta

from dateutil.parser import parse
from tzlocal import get_localzone

from component.Schedule import Schedule

from logger_config import report_logger
from Spider_Manager import ThreadSta


# 低内聚
class ClockThread(threading.Thread):
    """
    定时处理线程，用来处理在特定时间段修改爬取任务调度接口中的任务频率
    在start-end 之间的时间段采用fast_fqy ，其他采用slow_fqy
    周6 7维持高速
    """

    def __init__(self, schedule: Schedule,spiderManager):
        threading.Thread.__init__(self, name="clock", daemon=True)
        self.schedule = schedule
        self.spiderManager = spiderManager
        local_zone = get_localzone()
        self.start_date = local_zone.localize(parse(self.schedule.start))
        self.end_date = local_zone.localize(parse(self.schedule.end))

    def run(self):
        try:
            self.spiderManager.Clock_Sta = ThreadSta.Work
            self.check_date()
        except Exception:
            report_logger.error("Clock_Thread 线程出错")
            self.spiderManager.Clock_Sta = ThreadSta.Error

    def check_date(self):
        while True:
            if self.spiderManager.Clock_Sta == ThreadSta.Finish:
                break
            local_zone = get_localzone()
            curr_date = local_zone.localize(datetime.now())

            if curr_date.isoweekday() in [6, 7]:
                self.schedule.fcy_turn_fast()
            else:
                if self.schedule.over_night:
                    if self.start_date < curr_date < self.end_date:
                        self.schedule.fcy_turn_fast()
                    else:
                        self.schedule.fcy_turn_slow()
                else:
                    if self.start_date < curr_date < self.end_date:
                        self.schedule.fcy_turn_fast()
                    else:
                        self.schedule.fcy_turn_slow()
            time.sleep(1)


if __name__ == '__main__':
    schedule = Schedule("23:00", "6:00", 100, 10)
    clock = ClockThread(schedule)
    clock.start()
    clock.join()
