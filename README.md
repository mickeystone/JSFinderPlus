# JSFinderPlus

JSFinder是一款用作快速在网站的js文件中提取URL，子域名的工具。该工具在JSFinder上进行了增强，主要有：

- 多线程爬虫，支持深度爬取（爬取提取出的所有URL）
- 常见高危目录爆破
- 敏感信息（手机号、身份证号码等）识别
- 生成html报告，方便验证



# usage



```
PS D:\Code\python\JSFinderPlus> python  .\JSFinderPlus.py -h

     ____. ____________________.__            .___          __________.__
    |    |/   _____/\_   _____/|__| ____    __| _/__________\______   \  |  __ __  ______
    |    |\_____  \  |    __)  |  |/    \  / __ |/ __ \_  __ \     ___/  | |  |  \/  ___/
/\__|    |/        \ |     \   |  |   |  \/ /_/ \  ___/|  | \/    |   |  |_|  |  /\___ \
\________/_______  / \___  /   |__|___|  /\____ |\___  >__|  |____|   |____/____//____  >
                 \/      \/            \/      \/    \/                               \/

usage: python3 JSFinderPlus.py [options]

target:
  you must to specify target

  -u URL, --url URL     target URL (e.g. -u "http://example.com")

general:
  general options

  -h, --help            show this help message and exit
  -t NUM, --thread NUM  扫描线程，默认10
  -d                    对发现的URL进行查找，默认只查找输入的URL
  --open                立即打开报告
  --site-root ROOT      指定URL的根目录
  --proxy-socks SOCKS   socks proxy (e.g. --proxy-socks 127.0.0.1:1080)
  --proxy-http HTTP     http proxy (e.g. --proxy-http 127.0.0.1:8080)
  -c COOKIE             cookie
  --user-agent UA       you can customize the user-agent headers

examples:
  python3 JSFinderPlus.py -u http://example.com
  python3 JSFinderPlus.py -u http://example.com -d
  python3 JSFinderPlus.py -u http://example.com:7001/index --site-root http://example.com:7001/#/
  python3 JSFinderPlus.py -f list.txt -d -t 20
  python3 JSFinderPlus.py -f list.txt -o results.text
```



# example

python .\JSFinderPlus.py -u http://xx.xx.xx.xx -d --open

![1](https://user-images.githubusercontent.com/36331800/149890412-866f819e-ebd6-44d0-ba12-0f8bfd470983.png)



自动生成报告，点击url直接查看

![2](https://user-images.githubusercontent.com/36331800/149890520-8df16614-3157-4baf-b4ef-5828fb6e4e29.png)

