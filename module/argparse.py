#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse


def arg():
    parser = argparse.ArgumentParser(usage="python3 JSFinderPlus.py [options]", add_help=False)
    target = parser.add_argument_group("target", "you must to specify target")
    target.add_argument("-u", "--url", dest="url", type=str, help=" target URL (e.g. -u \"http://example.com\")")

    ge = parser.add_argument_group("general", "general options")
    ge.add_argument("-h", "--help", action="help", help="show this help message and exit")
    ge.add_argument("-t", "--thread", dest="thread_num", type=int, default=5, metavar='NUM',
                    help="扫描线程，默认10")

    ge.add_argument("-d", action='store_true', dest="deep", help="对发现的URL进行查找，默认只查找输入的URL")
    ge.add_argument("--open", action='store_true', help="立即打开报告")
    ge.add_argument("--site-root", type=str, dest="root", help="指定URL的根目录")

    ge.add_argument("--proxy-socks", dest="socks", type=str, help="socks proxy (e.g. --proxy-socks 127.0.0.1:1080)")
    ge.add_argument("--proxy-http", dest="http", type=str, help="http proxy (e.g. --proxy-http 127.0.0.1:8080)")
    ge.add_argument("-c", type=str, dest="cookie", help="cookie")
    ge.add_argument("--user-agent", dest="ua", type=str,
                    default="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 "
                            "Safari/537.36", help="you can customize the user-agent headers")

    example = parser.add_argument_group("examples")
    example.add_argument(action='store_false',
                         dest="python3 JSFinderPlus.py -u http://example.com\n  "
                              "python3 JSFinderPlus.py -u http://example.com -d\n  "
                              "python3 JSFinderPlus.py -u http://example.com:7001/index --site-root http://example.com:7001/#/\n  "
                              "python3 JSFinderPlus.py -f list.txt -d -t 20\n  "
                              "python3 JSFinderPlus.py -f list.txt -o results.text\n  "
                         )
    return parser.parse_args()
