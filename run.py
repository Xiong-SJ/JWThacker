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
from colorama import Fore

# 本地模块导入
import src.JWThacker_api as JWThacker

version="V 0.0.1"

def main():
    """主函数：程序入口逻辑"""
    parser = argparse.ArgumentParser()

    #查看版本
    parser.add_argument("--version",action="version",version=version)

    subparsers = parser.add_subparsers(dest="command")
    # 解码命令
    par_decode=subparsers.add_parser("decode",help="解码 JWT")
    par_decode.add_argument("token", type=str, help="编码的 JWT 字符串")


    # 编码命令
    par_encode=subparsers.add_parser("encode",help="编码 JWT")
    par_encode.add_argument("token", type=str, help="原 JWT 字符串")
    par_encode.add_argument("-p","--password",type=str,default=None,help="密码")
    par_encode.add_argument("--alg",type=str,default=None,help="需要的加密算法加密算法（若原 JWT 字符串中不含 alg 字段则需指定）")

    # TODO 暴力破解
    par_brute=subparsers.add_parser("brute",help="暴力破解 JWT 密码（还未开放）")
    par_brute.add_argument("token", type=str, help="编码的 JWT 字符串")
    par_brute.add_argument("-w","--wordlist", type=str, default=None, help="密码字典")

    # TODO 启用多进程加速
    parser.add_argument("-j", "--jobs", type=int, help="启用多进程加速（还未开放）")

    args = parser.parse_args()

    if not args.command in ["decode","encode","brute"]:
        parser.print_help()
        print(f"{Fore.RED}[-] 没有该 <{args.command}> command{Fore.RESET}")
        sys.exit(-1)

    if args.command == "decode":
        token_decode = JWThacker.JWT_decode(args.token)
        if token_decode is None :
            print(f"{Fore.RED}[-] 解码失败{Fore.RESET}", file=sys.stderr)
            sys.exit(-1)
        print(f"{Fore.GREEN}[+] <Success> : {token_decode}{Fore.RESET}")

    elif args.command == "encode":
        if args.alg =="None": args.alg=None
        token_decode = JWThacker.JWT_encode(args.token,password=args.password,algorithm=args.alg)
        if token_decode is None:
            print(f"{Fore.RED}[-] 加密失败{Fore.RESET}", file=sys.stderr)
            sys.exit(-1)
        print(f"{Fore.GREEN}[+] <Success> : {token_decode}{Fore.RESET}")

    elif args.command == "brute":
        token_decode = JWThacker.JWT_decode(args.token)
        wordlistpath = args.wordlist
        JWThacker.JWT_key_brute(token_decode,wordlistpath)

    else:  # brute 命令
        if args.token is None:
            print(f"{Fore.RED}[-] 请提供 JWT 字符串{Fore.RESET}")
            sys.exit(-1)
        if args.wordlist is None:
            print(f"{Fore.RED}[-] 请提供密码字典路径 (-w){Fore.RESET}")
            sys.exit(-1)
    
        print(f"{Fore.GREEN}[*] 开始暴力破解...{Fore.RESET}")
        result = JWThacker_api.JWT_key_brute(args.token, args.wordlist)
        if result:
            print(f"{Fore.GREEN}[+] 爆破成功！密钥: {result}{Fore.RESET}")
        else:
            print(f"{Fore.RED}[-] 未找到密钥{Fore.RESET}")
    else:
        pass



if  __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Fore.RED}[-] <ERROR>: {e}{Fore.RESET}",file=sys.stderr)