#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import socket
import sys

import socks

from module.color import color
from module.time import now


def proxy_set(pr, pr_mode):
    try:
        proxy_ip = str(re.search(r"(.*):", pr).group(1))
        proxy_port = int(re.search(r":(.*)", pr).group(1))
    except AttributeError:
        print(now.timed(de=0) + color.red_warn() + color.red(" Proxy format error (e.g. --proxy-socks 127.0.0.1:1080)"))
        sys.exit(0)
    if r"socks" in pr_mode:
        socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port)
    elif r"http" in pr_mode:
        socks.set_default_proxy(socks.HTTP, addr=proxy_ip, port=proxy_port)
    socket.socket = socks.socksocket
    print(now.timed(de=0) + color.yel_info() + color.yellow(" Use custom proxy: " + pr))
