#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'


from component.Save_Thread import SaveWorker


class OwSaveWorker(SaveWorker):
    def __init__(self, client):
        SaveWorker.__init__(self)
        self.client = client

    def result_save(self, params, item):
        suburb = params["Suburb"]
        state = params["State"]
        index = params["Index"]
        if item is False:
            self.client.update_task_record(suburb, state, False)
        else:
            item["Suburb"] = suburb
            item["State"] = state
            if self.client.insert_detail_page(item):
                self.client.update_task_record(suburb, state, int(index))


if __name__ == '__main__':
    pass
