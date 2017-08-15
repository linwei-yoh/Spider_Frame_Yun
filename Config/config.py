# coding=utf-8

abuyun_config = {
    # 代理服务器
    "proxyHost": "http-dyn.abuyun.com",
    "proxyPort": "9020",
    # 代理隧道验证信息
    "proxyUser": "H0N23XKN5YK3B7KD",
    "proxyPass": "31BCF4A4143D6CE2",
}


DB_config = {
    'db_type': 'redis',

    'mysql': {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'charset': 'utf8',
    },
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'password': '',
        'db': 1,
    },
    'mongodb': {
        'host': 'localhost',
        'port': 27017,
        'username': '',
        'password': '',
    }
}

Spider_config = {
    "thread_num": 10,  # 爬取线程数量
    "parser_num": 1,  # 解析进程数量
    "retry_times": 10,  # 网址访问失败最大重试次数
    "monitor_time": 5,  # 监视报告线程 报告间隔周期(s)
    "fetch_interval": 1,  # 爬取任务载入周期(s)
    "fast_fcy": 5,  # 在快速爬取时间段，每个载入周期需要载入的任务数量
    "nor_fcy": 5,  # 在常规爬取时间段，每个载入周期需要载入的任务数量
    "fast_start": "23:00:00",  # 快速爬取时间段的起始时间
    "fast_end": "6:00:00",  # 快速爬取时间段的结束时间
}


data_base = 'realestateview'
rent_table = 'rv_rent'
sold_table = "rv_sold"

ipproxy_check_set = "check_set"
free_ipproxy_table = 'free_ipproxy'
