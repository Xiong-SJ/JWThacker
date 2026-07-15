#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/7/9 23:36
# @Author  : YISHI
# @File    : run.py
# @Software: PyCharm

# 标准库导入
import argparse
import sys

# 第三方库导入
# import requests

# 本地模块导入
import src.JWThacker as JWThacker

version="v 0.0.1"

def main():
    """主函数：程序入口逻辑"""
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")
    # 解码命令
    par_decode=subparsers.add_parser("decode",help="解码 JWT")
    par_decode.add_argument("token", type=str, help="编码的 JWT 字符串")


    # 编码命令
    par_encode=subparsers.add_parser("encode",help="编码 JWT")
    par_encode.add_argument("token", type=str, help="原 JWT 字符串")
    par_encode.add_argument("-p","--password",type=str,default=None,help="密码")
    par_encode.add_argument("--alg",type=str,default=None,help="需要的加密算法（若原 JWT 字符串中包含就不需要写）")

    # TODO 暴力破解
    par_brute=subparsers.add_parser("brute",help="暴力破解 JWT 密码（还未开放）")
    par_brute.add_argument("token", type=str, help="编码的 JWT 字符串")
    par_brute.add_argument("-w","--wordlist", type=str, default=None, help="密码字典")

    # TODO 启用GPU加速
    parser.add_argument("--gpu", action="store_true", help="启用GPU加速（还未开放）")

    args = parser.parse_args()

    if not args.command in ["decode","encode","brute"]:
        parser.print_help()
        print(f"[-] 没有该 <{args.command}> command")
        sys.exit(-1)

    if args.command == "decode":
        token_decode = JWThacker.JWT_decode(args.token)
        if token_decode is None :
            print("[-] 解码失败", file=sys.stderr)
            sys.exit(-1)
        print(token_decode)

    elif args.command == "encode":
        if args.alg =="None": args.alg=None
        token_decode = JWThacker.JWT_encode(args.token,password=args.password,algorithm=args.alg)
        if token_decode is None:
            print("[-] 加密失败", file=sys.stderr)
            sys.exit(-1)
        print(token_decode)

    else:
        pass



if  __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[-] <ERROR>: {e}",file=sys.stderr)
