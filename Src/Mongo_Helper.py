#!/usr/bin/env python4
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from pymongo import MongoClient
import pymongo.errors
import pymongo
from datetime import datetime
from component.logger_config import report_logger as logger

from Config import config


class MongoHelper(object):
    def __init__(self):
        mongo_config = config.DB_config.get("mongodb", None)

        self.client = MongoClient(mongo_config["host"], mongo_config["port"])
        self.database = self.client[config.data_base]
        self.rent_table = self.database[config.rent_table]
        self.sold_table = self.database[config.sold_table]
        self.create_index()
        self.update_date = datetime.utcnow()

    def recreate(self):
        """
        慎用！ 删除一个数据库的内容，重新建立表和索引  慎用！
        :return: T/F
        """
        self.client.drop_database(self.database)
        return self.create_index()

    def create_index(self):
        """
        建立唯一索引索引 
        :return: T/F
        """
        # 对一个表建立 复合 唯一索引，且在后台执行
        # dropDups在3.0和之后的mongodb中不再被支持，遇到重复文档则会报错

        try:
            self.rent_table.create_index([("pid", pymongo.ASCENDING)], background=True)
            self.sold_table.create_index([("pid", pymongo.ASCENDING)], background=True)
        except pymongo.errors.DuplicateKeyError:
            print("创建索引失败，已存在重复数据")
            logger.error("创建索引失败")
            return False
        except Exception:
            return False
        return True

    def inset_result_many(self, items, key):
        try:
            if key == "Rent":
                for item in items:
                    item["timestamp"] = self.update_date
                    item['otm_flag'] = 1  # 0:not find 1:on market
                    self.rent_table.update_one({"pid": item["pid"]}, {"$set": item}, upsert=True)
            elif key == "Sold":
                for item in items:
                    item["timestamp"] = self.update_date
                    item['otm_flag'] = 1
                    self.sold_table.update_one({"pid": item["pid"]}, {"$set": item}, upsert=True)
            return True
        except Exception as e:
            logger.error("insert detail page faile " + str(e))
            return False

    def update_otm_flag(self):
        self.rent_table.update_many({"timestamp": {"$ne": self.update_date}}, {"$set": {'otm_flag': 0}})
        self.sold_table.update_many({"timestamp": {"$ne": self.update_date}}, {"$set": {'otm_flag': 0}})


if __name__ == '__main__':
    # 慎用
    MongoDB = MongoHelper()

    MongoDB.recreate()
