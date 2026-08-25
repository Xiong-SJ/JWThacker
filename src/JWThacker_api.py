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
        jwt=jwt.split(".")
        jwt_header = json.loads(jwt[0])
        jwt_pyload = json.loads(jwt[1])
    elif re.fullmatch(r"\{[^}]*\}", jwt):
        jwt_pyload=json.loads(jwt)
    else:
        print(f"{Fore.RED}[-] <ERROR>: JWT格式错误{Fore.RESET}", file=sys.stderr)
        return None

    return JWTcode.jwt_encode(jwt_header,jwt_pyload,password)

# TODO
def JWT_key_brute(token, wordlist_path, max_workers):
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            keys = [line.strip() for line in f if line.strip()]
        
        print(f"[*] 字典共 {len(keys)} 个密钥，使用 {max_workers} 个线程")
        
        found_key = None
        
        def try_key(key):
            if JWTcode.examine_jwt(token, key):
                return key, True
            return key, False
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(try_key, k): k for k in keys}
            for future in as_completed(futures):
                key, success = future.result()
                if success:
                    found_key = key
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
        
        if found_key:
            print(f"[+] 找到密钥: {found_key}")
            payload = JWTcode.jwt_decode(token)
            print(f"[+] 解密后 Payload: {payload}")
            return found_key
        else:
            print("[-] 未找到有效密钥")
            return None
            
    except Exception as e:
        print(f"[-] 错误: {e}")
        return None

def main():
    pass


if __name__ == "__main__":
    main()
