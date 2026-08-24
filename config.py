#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24 22:19
# @Author  : YISHI
# @Email   : wowoxiongsj123123@outlook.com
# @File    : config.py
# @Software: PyCharm

# 查看第三方库是否安装
def check_package(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        print(f"{package_name} 未安装")
        print(f"请执行pip install -r requirements.txt")
        return False

def main():
    """主函数：程序入口逻辑"""
    IS_RUN=True

    if not check_package("authlib")       : IS_RUN=False
    if not check_package("cffi")          : IS_RUN=False
    if not check_package("colorama")      : IS_RUN=False
    if not check_package("cryptography")  : IS_RUN=False
    if not check_package("joserfc")       : IS_RUN=False
    if not check_package("pycparser")     : IS_RUN=False

    if not IS_RUN : exit(-1)


main()
