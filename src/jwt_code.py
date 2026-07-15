#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/7/9 23:38
# @Author  : YISHI
# @File    : jwt_code.py
# @Software: PyCharm


# 标准库导入
import sys
import base64
import binascii
import json
from datetime import datetime, timedelta
import warnings

# 第三方库导入
import jwt
from colorama import init, Fore, Style

# 本地模块导入
# from utils import helper

#忽略警告
warnings.filterwarnings("ignore", message=".*below the minimum recommended length.*")

class JWTcode:
    @staticmethod
    def  _b64url_decode(data: str) -> str:
        """内部工具：补全填充后执行 Base64URL 解码，返回 UTF-8 字符串"""
        # 补全 = 填充，使长度为4的倍数
        padding = 4 - len(data) % 4
        if padding != 4:
            data += "=" *padding
        # 解码并转字符串
        return base64.urlsafe_b64decode(data).decode("utf-8")

    @staticmethod
    def jwt_decode(data:str) -> str | None:
        """
        :param data: string data to encode
        :return: 解码成功返回str，失败返回None
        """
        jwt_string=data.split('.')

        if len(jwt_string) != 3:
            print(f"{Fore.RED}[-] <ERROR>: Perhaps this isn't JWT.{Fore.RESET}",file=sys.stderr)
            return None
        try:
            jwt_string[0] = JWTcode._b64url_decode(jwt_string[0])
            jwt_string[1] = JWTcode._b64url_decode(jwt_string[1])
            return '.'.join(jwt_string)
        except binascii.Error as e:
            print(f"{Fore.RED}[-] <ERROR>: Decoding failed! {e}{Fore.RESET}",file=sys.stderr)
            return None
        except Exception as e:
            print(f"{Fore.RED}[-] <ERROR>: {e}{Fore.RESET}",file=sys.stderr)
            return None

    @staticmethod
    def jwt_encode(jwt_str:str,password:str|None=None) -> str | None:
        """
        :param jwt_str: 未加密的JWT
        :param password: JWT的加密的密码
        :return: 加密的JWT，失败返回 None
        """
        jwt_list=jwt_str.split('.')
        jwt_list[0] = json.loads(jwt_list[0])
        jwt_list[1] = json.loads(jwt_list[1])
        try:
            if jwt_list[0]["alg"] is None:
                password=None
            token = jwt.encode(payload=jwt_list[1],key=password,algorithm=jwt_list[0]["alg"])
            return token
        except Exception as e:
            print(f"{Fore.RED}[-] <ERROR>: {e}{Fore.RESET}",file=sys.stderr)
            return None

    @staticmethod
    def examine_jwt(jwt_str:str,password:str|None=None) -> bool | None:
        jwt_list = jwt_str.split('.')
        try:
            jwt_list[0] = json.loads(jwt_list[0])
            jwt_list[1] = json.loads(jwt_list[1])
            token = jwt.encode(payload=jwt_list[1], key=password, algorithm=jwt_list[0]["alg"])
            token = token.split('.')[-1]

            return True if token == jwt_list[-1] else False
        except Exception as e:
            print(f"{Fore.RED}[-] <ERROR>: {e}{Fore.RESET}", file=sys.stderr)
            return None




def main():
    """主函数：程序入口逻辑"""
    secret_key = "your-256-bit-secret"
    payload = {
        "sub": "user_123",
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    # 生成带HS256签名的令牌
    token = jwt.encode(payload, secret_key, algorithm = "HS256")
    print(token)
    t=JWTcode.jwt_decode(token)
    print(t)
    print(JWTcode.examine_jwt(t,secret_key))

if __name__ == "__main__":
    main()
