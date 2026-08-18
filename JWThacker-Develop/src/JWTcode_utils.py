#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/7/9 23:38
# @Author  : YISHI
# @File    : JWTcode_utils.py
# @Software: PyCharm


# 标准库导入
import sys
import base64
import binascii
import json
import warnings

# 第三方库导入
from joserfc import jwt
import joserfc.errors as jwt_errors
from joserfc.jwk import OctKey, RSAKey, ECKey
from colorama import Fore

# 本地模块导入
# from utils import helper

#忽略警告
warnings.filterwarnings("ignore", message="Key size should be >= 112 bits")


def jwt_encode(head:dict|None,payload:dict|None,password:str|None,jwt_str:str|None=None) -> str | None:
    # 兼容老代码
    """
    :param head: JWT's HEAD
    :param payload:JWT's Payload
    :param jwt_str: (兼容老代码) 未加密的JWT -> header.password
    :param password: JWT的加密的密码
    :return: 加密的JWT，失败返回 None
    """
    if not jwt_str is None:
        jwt_list=jwt_str.split('.')
        header_dict  = json.loads(jwt_list[0])
        payload_dict = json.loads(jwt_list[1])
    elif not payload is None:
        header_dict  = {"typ":"JWT","alg":'HS'} if head is None else head
        payload_dict = payload
    else:
        print(f"{Fore.RED}[-] <ERROR>: When jwt_str is None , the payload can not be `None`",file=sys.stderr)
        return None

    if 'alg' not in header_dict:
        print(f"{Fore.RED}[-] <ERROR>: No key is `alg` in header",file=sys.stderr)
        return None

    try:
        if header_dict['alg'] in ['None','none']:
            header_dict['alg']='none'
            header_json = json.dumps(header_dict, separators=(',', ':'), ensure_ascii=False)
            payload_json = json.dumps(payload_dict, separators=(',', ':'), ensure_ascii=False)

            header_b64 = base64.urlsafe_b64encode(header_json.encode('utf-8')).decode('utf-8').rstrip('=')
            payload_b64 = base64.urlsafe_b64encode(payload_json.encode('utf-8')).decode('utf-8').rstrip('=')
            return f'{header_b64}.{payload_b64}.'

        if password is None:
            print(f"{Fore.RED}[-] <ERROR>: When alg is {header_dict['alg']} , the passwd can not be `None`",file=sys.stderr)
            return None

        if   header_dict['alg'][:2] == "HS":
            # 对称加密 (HMAC) -> OctKey
            key = OctKey.import_key(password.encode("utf-8"))

        elif header_dict['alg'][:2] == "RS":
            # 非对称加密 (RSA) -> RSAKey
            # 注意：key_str 必须是标准的 RSA 私钥 PEM 字符串
            key = RSAKey.import_key(password.encode("utf-8"))

        elif header_dict['alg'][:2] == "ES":
            # 椭圆曲线 (ECDSA) -> ECKey
            # 注意：key_str 必须是标准的 EC 私钥 PEM 字符串
            key = ECKey.import_key(password.encode("utf-8"))
        else:
            print(header_dict['alg'][:2])
            print(f"{Fore.RED}[-] <ERROR>: unsupported algorithm `{header_dict['alg']}`{Fore.RESET}",file=sys.stderr)
            return None

        token=jwt.encode(header_dict,payload_dict,key)
        return token

    except jwt_errors.UnsupportedAlgorithmError:
        print(f"{Fore.RED}[-] <ERROR>: unsupported algorithm `{header_dict['alg']}`{Fore.RESET}",file=sys.stderr)
        return None

    except Exception as e:
        print(f"{Fore.RED}[-] <ERROR>: {e}{Fore.RESET}",file=sys.stderr)
        return None


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
        jwt_string[0] = _b64url_decode(jwt_string[0])
        jwt_string[1] = _b64url_decode(jwt_string[1])
        return '.'.join(jwt_string)
    except binascii.Error as e:
        print(f"{Fore.RED}[-] <ERROR>: Decoding failed! {e}{Fore.RESET}",file=sys.stderr)
        return None
    except Exception as e:
        print(f"{Fore.RED}[-] <ERROR>: {e}{Fore.RESET}",file=sys.stderr)
        return None


def  _b64url_decode(data: str) -> str:
    """内部工具：补全填充后执行 Base64URL 解码，返回 UTF-8 字符串"""
    # 补全 = 填充，使长度为4的倍数
    padding = 4 - len(data) % 4
    if padding != 4:
        data += "=" *padding
    # 解码并转字符串
    return base64.urlsafe_b64decode(data).decode("utf-8")


def examine_jwt(jwt_str:str,password:str|None=None) -> bool | None:
    """
    :param jwt_str: 加密的JWT
    :param password: 要尝试JWT的加密的密码
    :return: 密码正确返回True,否则返回False,错误返回None
    """
    jwt_str= jwt_decode(jwt_str)
    if jwt_str is None:
        return None
    jwt_list = jwt_str.split('.')
    try:
        header_dict  = json.loads(jwt_list[0])
        payload_dict = json.loads(jwt_list[1])
        token = jwt_encode(header_dict,payload_dict,password)
        if token is None:
            return None
        token = token.split('.')[-1]

        return True if token == jwt_list[-1] else False
    except Exception as e:
        print(f"{Fore.RED}[-] <ERROR>: {e}{Fore.RESET}", file=sys.stderr)
        return None


def main():
    pass

if __name__ == "__main__":
    main()
