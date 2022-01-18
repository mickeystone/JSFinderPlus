#!/usr/bin/env python"
# coding: utf-8
# By Threezh1
# https://threezh1.github.io/
import os
import queue
import re
from urllib.parse import urlparse

import urllib3

from core.FindThread import UrlProcuder, UrlConsumer, InfoOutput, ScanThread
from core.core import Core
from module import globals
from module.argparse import arg
from module.banner import banner
from module.color import color
from module.proxy import proxy_set


def load_globals(args):
    header = {
        'Accept': 'application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, '
                  'application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
        'User-agent': args.ua,
        'Cookie': args.cookie,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'close'
    }
    globals.init()  # 初始化全局变量模块
    globals.set_value("HEADERS", header)
    globals.set_value("URL", args.url)
    globals.set_value("OPEN", args.open)
    globals.set_value("ROOT_PATH", os.path.abspath('.'))
    if args.root:
        if args.root.endswith("/"):
            globals.set_value("SITE_ROOT", args.root[:-1])
        globals.set_value("SITE_ROOT", args.root)

    globals.set_value("IS_DEEP", args.deep)
    globals.set_value("ALL_LIST", [])
    globals.set_value("SUBDOMIAN_LIST", [])
    globals.set_value("leak_infos_match", [])

    if args.url:
        filename = urlparse(args.url).hostname
        if not os.path.exists("output"):
            os.makedirs("output")
        filename = re.sub(re.compile('[/\\\:*?"<>|]'), "_", filename)
        globals.set_value("FILE_PATH", "output\\" + filename + ".html")


if __name__ == "__main__":
    urllib3.disable_warnings()
    print(banner)
    args = arg()
    load_globals(args)  # 加载全局变量
    if args.socks:
        proxy_set(args.socks, "socks")  # proxy support socks5 http https
    elif args.http:
        proxy_set(args.http, "http")  # proxy support socks5 http https

    num_pool = []
    url_queue = queue.Queue(100000)
    text_queue = queue.Queue(100000)
    output_queue = queue.Queue(1000000)
    globals.set_value("OUT_QUEUE", output_queue)
    if args.url:
        url_queue.put(args.url)
        globals.get_value("ALL_LIST").append(args.url)
    else:
        print(color.red_error() + "缺少必要参数，请检查-u")
        exit(0)

    t_num = args.thread_num  # 生产线程数量
    t_list = []

    # 先消费初始url，根据html在生产其他url
    for x in range(t_num):
        t = UrlConsumer(name='消费线程-%d' % x, url_queue=url_queue, text_queue=text_queue)
        t_list.append(t)
        t.start()

    for x in range(t_num):
        t = UrlProcuder(name='生产线程-%d' % x, url_queue=url_queue, text_queue=text_queue)
        t_list.append(t)
        t.start()

    scan_queue = queue.Queue(1000)
    # 扫描高危目录
    with open(globals.get_value("ROOT_PATH") + "/module/dict.txt", "r", encoding='utf-8') as f:
        line = f.readline()
        while line:
            scan_queue.put(Core.process_url(args.url, line.replace("\n", "")))
            line = f.readline()

    for x in range(5):
        t = ScanThread(name='扫描高危路径-%d' % x, scan_queue=scan_queue)
        t_list.append(t)
        t.start()

    # 信息输出线程
    t = InfoOutput(name='信息输出线程-%d' % 1, output_queue=output_queue)
    t_list.append(t)
    t.start()



    for t in t_list:
        t.join()
