#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/7/15 12:35
# @Author  : YISHI
# @File    : JWThacker.py
# @Software: PyCharm

# 标准库导入
import re
import sys
import json

# 第三方库导入
# import requests

# 本地模块导入
from src.jwt_code import JWTcode


def JWT_decode(token:str) -> str|None:
    """
    :return: 解码成功返回str，失败返回None
    """
    return JWTcode.jwt_decode(token)

def JWT_encode(jwt:str,password:str|None=None,algorithm:str|None=None) -> str|None:
    """
    :return: 解码成功返回str，失败返回None
    """

    if re.fullmatch(r"\{[^}]*\}\.\{[^}]*\}", jwt):
        jwt_str=jwt
    elif re.fullmatch(r"^\{[^}]*\}$", jwt):
        jwt_alg = json.dumps({
            "alg": algorithm
        })
        jwt_payload = jwt
        jwt_str=jwt_alg+'.'+jwt_payload
    else:
        print(f"[-] <ERROR>: JWT格式错误", file=sys.stderr)
        return None

    return JWTcode.jwt_encode(jwt_str,password)


def main():
    """主函数：程序入口逻辑"""
    pass


if __name__ == "__main__":
    main()
