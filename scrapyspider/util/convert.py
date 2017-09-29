#/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import hashlib
from collections import OrderedDict

conv = OrderedDict()

"""按顺序替换文档中的内容"""
conv['(<pre.*?><code>)|(</code></pre>)'] = '\n```\n'        # 多行代码
conv['(</?code>)|(</?kbd>)'] = '`'                          # 代码突出
conv['<li>'] = '* '                                         # 列表
conv['(</?strong>)'] = '**'                                 # 加粗
conv['(<em>)|(</em>)'] = '_'                                # 斜体
conv['</p>'] = '\n'
conv['<[Hh]1>'] = '### '
conv['<[Hh][2-4]>'] = '#### '
conv['<.*?>'] = ''
conv['&lt;'] = '<'
conv['&gt;'] = '>'
conv['\r\n'] = '\n'
conv['\n{2,}'] = '\n\n'


def html2md(html):
    """将 stackoverflow document 详细条目的 html 转化成 markdown 格式"""
    content = html
    for key, value in conv.items():
        content = re.sub(key, value, content)
    
    return content


def MD5(string):
    """MD5 加密[大写]"""
    return hashlib.md5(string.encode('utf8')).hexdigest().upper()