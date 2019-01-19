#!/usr/bin/env python
# -*- coding:utf-8 -*-
# create by y1ang
# create date  2019.01.20 - 00:20
# desc 全书网小说连载内容下载。io文件输出

import urllib2
import re

# __auth__全书网小说下载

# 小说章节地址
chapte_url_list = []
# 小说章节名称
chapte_name_list = []


def get_html(url):
    req = urllib2.Request(url)
    html = urllib2.urlopen(req).read().decode('gbk')
    novel_info = {}
    # 小说标题
    novel_info['title'] = re.findall(r'<div class="chapName">.*?<strong>(.*)</strong>', html)[0]
    # 小说作者
    novel_info['author'] = re.findall(r'<div class="chapName"><span class="r">(.*?)</span>', html)[0]
    # 内容
    content = re.findall(r'<DIV class="clearfix dirconone">(.*?)</DIV>', html, re.S | re.I)[0]

    tag_a = re.findall(r'<a.*?</a>', content)

    fiction = re.findall(r'<DIV class=dirtitone><H2>(.*?)</H2></div>', html, re.S)[0]

    # 循环获取小说地址
    for i in tag_a:
        chapte_url = i.split(',')[0]
        # 小说章节地址
        tag_a_url = re.findall(r'<a href="(.*)" title=".*?">.*?</a>', chapte_url)[0]
        # 小说章节名称
        chapte_name = re.findall(r'title="(.*)"', chapte_url)[0]

        chapte_url_list.append(tag_a_url)
        chapte_name_list.append(chapte_name)

    return fiction


def get_chapter(c_url):
    chapte_con = urllib2.urlopen(urllib2.Request(c_url)).read().decode('gbk')
    chapte = \
        re.findall(
            r'div class="mainContenr"   id="content"><script type="text/javascript">style.\(\);</script>(.*?)</div>',
            chapte_con, re.S)[0]
    chapte = chapte.replace('&nbsp;', '')
    chapte = chapte.replace('<br />', '')
    return chapte


def down(name, filepath):
    j = 0
    for i in chapte_url_list:
        title = '\n\n\n\n' + chapte_name_list[j].encode('gbk') + '\n\n'
        with open(filepath + name + '.txt', 'a')as f:
            f.write(title)
            conn = get_chapter(i).encode('gbk')
            conn = conn.replace('<script type="text/javascript">style6();</script>', '\n')
            f.write(str(conn))

        print '正在下载:' + str(chapte_name_list[j].encode('utf-8'))
        j += 1
    print '下载完成'


if __name__ == '__main__':
    '''传入需要下载的小说的地址'''
    name = get_html('http://www.quanshuwang.com/book/6/6363')
    filepath = "C:/Users/stark/Desktop/"
    down(name, filepath)
