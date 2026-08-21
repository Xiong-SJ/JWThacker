#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/7/15 12:35
# @Author  : YISHI
# @File    : JWThacker_api.py
# @Software: PyCharm

# 标准库导入
import re
import sys
import json

# 第三方库导入
from colorama import Fore


# 本地模块导入
import src.JWTcode_utils as JWTcode


def JWT_decode(token:str) -> str|None:
    """
    :return: 解码成功返回str，失败返回None
    """
    return JWTcode.jwt_decode(token)

def JWT_encode(jwt:str,password:str|None=None,algorithm:str|None=None) -> str|None:
    """
    :return: 解码成功返回str，失败返回None
    """
    jwt_header = {
        "alg": algorithm,
        "typ": "JWT"
    }

    if re.fullmatch(r"\{[^}]*\}\.\{[^}]*\}", jwt):
        jwt_pyload=json.loads(jwt)
    else:
        print(f"{Fore.RED}[-] <ERROR>: JWT格式错误{Fore.RESET}", file=sys.stderr)
        return None

    return JWTcode.jwt_encode(jwt_header,jwt_pyload,password)

# TODO
def JWT_key_brute():
    pass


def main():
    pass


if __name__ == "__main__":
    main()
