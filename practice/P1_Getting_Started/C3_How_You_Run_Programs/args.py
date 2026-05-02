#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/4

"""show my arguments too"""

import sys

print(sys.version.split()[0])
print(sys.argv)

# test part
if __name__ == '__main__':
    print('只有作为顶层文件执行才会见到这句话！')
