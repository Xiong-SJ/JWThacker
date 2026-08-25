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
def JWT_key_brute(token, wordlist_path, max_workers=None):
    import jwt
    from multiprocessing import Pool, cpu_count
    
    try:
        header = jwt.get_unverified_header(token)
        alg = header.get('alg', 'HS256')
        
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            keys = [line.strip() for line in f if line.strip()]
        
        if max_workers is None:
            max_workers = cpu_count()
        
        print(f"[*] 字典共 {len(keys)} 个密钥，使用 {max_workers} 个进程")
        print(f"[*] 检测到算法: {alg}")
        
        found_key = None
        
        def try_key(key):
            if examine_jwt(token, key):
                return key, True
            return key, False
        
        with Pool(processes=max_workers) as pool:
            results = pool.map(try_key, keys)
            for key, success in results:
                if success:
                    found_key = key
                    pool.terminate()
                    break
        
        if found_key:
            print(f"[+] 找到密钥: {found_key}")
            payload = jwt.decode(token, found_key, algorithms=[alg])
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
