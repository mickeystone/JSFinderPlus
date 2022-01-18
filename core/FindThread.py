import os
import queue
import threading
import time

from core.core import Core
from module import globals
from module.color import color


class UrlProcuder(threading.Thread):
    """
    生产者，获取URL
    """

    def __init__(self, name, url_queue: queue.Queue, text_queue: queue.Queue, *args, **kwargs):
        super(UrlProcuder, self).__init__(*args, **kwargs)
        self.name = name
        self.url_queue = url_queue
        self.text_queue = text_queue

    def run(self):
        while True:
            try:
                # 等待5秒，没数据就退出
                url, html, code = self.text_queue.get(block=True, timeout=15)
                globals.get_value("OUT_QUEUE").put((1, url, code, html))

                if globals.get_value("IS_DEEP") or url == globals.get_value("URL"):
                    #  页面不为空
                    # 获取页面中herf
                    links = Core.find_by_url_deep(html, url)
                    # 正则匹配
                    links2 = Core.find_by_url(html, url)

                    for link in links:
                        if link not in globals.get_value("ALL_LIST"):
                            globals.get_value("OUT_QUEUE").put((2, link, 0, ""))
                            # 深度扫描
                            globals.get_value("ALL_LIST").append(link)
                            self.url_queue.put(link)
                    for link in links2:
                        if link not in globals.get_value("ALL_LIST"):
                            globals.get_value("OUT_QUEUE").put((2, link, 0, ""))
                            globals.get_value("ALL_LIST").append(link)
                            self.url_queue.put(link)
            except Exception as e:
                break


class UrlConsumer(threading.Thread):
    """
    消费者，发送请求，获取文本信息
    """

    def __init__(self, name, url_queue: queue.Queue, text_queue: queue.Queue, *args, **kwargs):
        super(UrlConsumer, self).__init__(*args, **kwargs)
        self.name = name
        self.url_queue = url_queue
        self.text_queue = text_queue

    def run(self):
        while True:
            try:
                url = self.url_queue.get(block=True, timeout=15)
                html, code = Core.Extract_html(url)
                if html:
                    self.text_queue.put((url, html, code))
            except Exception as e:
                break


class ScanThread(threading.Thread):
    """
    消费者，发送请求，获取文本信息
    """

    def __init__(self, name, scan_queue: queue.Queue, *args, **kwargs):
        super(ScanThread, self).__init__(*args, **kwargs)
        self.name = name
        self.scan_queue = scan_queue

    def run(self):
        while True:
            try:
                if self.scan_queue.empty():
                    break
                url = self.scan_queue.get(block=True, timeout=15)
                html, code = Core.Extract_html(url)
                if code != 404:
                    globals.get_value("OUT_QUEUE").put((4, url, code, html))
            except Exception as e:
                break


class InfoOutput(threading.Thread):
    """
    消费者，发送请求，获取文本信息
    """

    def __init__(self, name, output_queue: queue.Queue, *args, **kwargs):
        super(InfoOutput, self).__init__(*args, **kwargs)
        self.name = name
        self.output_queue = output_queue

    def run(self):
        # 文本输出
        successUrlList = []
        errorUrlList = []
        jsList = []
        otherUrlList = []
        riskList = []
        while True:
            try:
                type, url, code, text = self.output_queue.get(block=True, timeout=15)
                if type == 1:
                    if code == 200:
                        print(color.green("[*] URL:{} --- code:{} -- size:{}".format(url, str(code), str(len(text)))))
                        if url.endswith(".js") or url.endswith(".css") or url.endswith(".ico") or url.endswith(
                                ".png") or url.endswith("jpg"):
                            jsList.append((url, code, len(text)))
                        else:
                            successUrlList.append((url, code, len(text)))
                    # 可能是拼接不对
                    elif code == 404:
                        errorUrlList.append((url, code, len(text)))
                    else:
                        print(color.magenta("[*] URL:{} --- code:{} -- size:{}".format(url, str(code), str(len(text)))))
                        otherUrlList.append((url, code, len(text)))
                elif type == 2:
                    print("[-] Find URL:{}".format(url))

                # 发现敏感信息
                elif type == 3:
                    print(color.blue("[-] Find leak info ==>{}".format(text)))
                # 发现高危目录
                elif type == 4:
                    print(color.red("[*] Find High Risk URL:{}".format(url)))
                    riskList.append((url, code, len(text)))
            except Exception as e:
                print(e)
                break

        # 生成报告
        errorUrlList.sort(key=lambda x: x[2], reverse=True)
        otherUrlList.sort(key=lambda x: x[2], reverse=True)
        riskList.sort(key=lambda x: x[2], reverse=True)
        successUrlList.sort(key=lambda x: x[2], reverse=True)

        table = """
         <tr class="ant-table-row ant-table-row-level-0"
                                                            data-row-key="0">
                                                            <td class="ant-table-row-expand-icon-cell">
                                                                <div role="button" tabindex="0" aria-label="Expand row"
                                                                     class="ant-table-row-expand-icon ant-table-row-collapsed"></div>
                                                            </td>
                                                            <td class="ant-table-row-cell-break-word">{id}</td>
                                                            <td class="ant-table-column-has-actions ant-table-column-has-sorters">
                                                                <a href="{url}" target="_blank" 
                                                                   style="display: inline-block; max-width: 50vw;">
                                                                    {url} </a></td>
                                                            <td class="ant-table-column-has-actions ant-table-column-has-filters ant-table-column-has-sorters filter-column">
                                                                {info}
                                                            </td>
                                                            <td class="ant-table-column-has-actions ant-table-column-has-sorters">
                                                                {time}
                                                            </td>
                                                        </tr>
                                                        
        """

        html_end = """
                                                                </tbody>


                                                    </table>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div><!----><!----></main>
            <footer class="ant-layout-footer" style="text-align: center;"><a href="https://xray.cool" target="_blank">Powered
                by ROC-L</a></footer>
        </section><!----></div>
</div>

</body>

</html>
        """

        id = 1
        tables = ""

        # 输出子域名
        if globals.get_value("SUBDOMIAN_LIST"):
            print(color.yellow("[+] Find Subdomian:"))
            for line in globals.get_value("SUBDOMIAN_LIST"):
                print(color.yellow(line))
                tables = tables + (
                    table.format(id=str(id), url=line, info="subdomain",
                                 time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

        # 高危目录
        for url, code, l in riskList:
            tables = tables + (table.format(id=str(id), url=url, info="code:{} -- size:{}".format(str(code), str(l)),
                                            time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            id = id + 1

        # 敏感信息
        for k, m, url in globals.get_value("leak_infos_match"):
            tables = tables + (table.format(id=str(id), url=url, info="{} / {}".format(str(k), str(m)),
                                            time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

        # 发信访问成功目录
        for url, code, l in successUrlList:
            tables = tables + (table.format(id=str(id), url=url, info="code:{} -- size:{}".format(str(code), str(l)),
                                            time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            id = id + 1

        #
        for url, code, l in otherUrlList:
            tables = tables + (
                table.format(id=str(id), url=url, info="code:{} -- size:{}".format(str(code), str(l)),
                             time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            id = id + 1

        for url, code, l in errorUrlList:
            tables = tables + (
                table.format(id=str(id), url=url, info="code:{} -- size:{}".format(str(code), str(l)),
                             time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            id = id + 1

        for url, code, l in jsList:
            tables = tables + (
                table.format(id=str(id), url=url, info="code:{} -- size:{}".format(str(code), str(l)),
                             time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            id = id + 1

        html = ""
        with open(globals.get_value("ROOT_PATH") + "/module/report.html", "r", encoding='utf-8') as f:
            html = f.read()

        with open(globals.get_value("ROOT_PATH") + "/" + globals.get_value("FILE_PATH"), "w", encoding='utf-8') as w:
            content = html + tables + html_end
            w.write(content)

        print(color.green("报告生成成功！位置：") + globals.get_value("ROOT_PATH") + "/" + globals.get_value("FILE_PATH"))

        if globals.get_value("OPEN"):
            os.system("start " + globals.get_value("ROOT_PATH") + "\\" + globals.get_value("FILE_PATH"))
