# JWThacker

> JWT 安全测试工具 —— 解码、伪造、暴力破解 JWT Token

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

JWThacker 是一个基于 Python 的 JWT（JSON Web Token）安全测试工具，支持 JWT 的**解码**、**重新编码（伪造）**，并计划支持**暴力破解**与 **多进程加速**功能。适用于 CTF 竞赛、渗透测试及安全研究场景。

---

## 功能特性

- **支持算法**:对称加密（如 HS256）、非对称加密（如 RS256、RS512）和椭圆曲线加密（如 ES256、ES384）
- **JWT 解码**：将 JWT 的 Header 和 Payload 部分进行 Base64URL 解码，还原可读的 JSON 内容
- **JWT 编码**：支持修改 Payload 后重新签名，可指定算法（alg）和密钥（password）
- **暴力破解**：通过字典爆破 JWT 密钥
- **启用多进程加速**：使用多进程通过字典爆破 JWT 密钥

---

## 项目结构

```
JWThacker/
├── run.py                 # 命令行入口
├── requirements.txt       # 项目依赖
├── config.py              # 配置文件
├── wordlist.txt           # 默认密码字典
├── src/
│   ├── __init__.py        # 包初始化
│   ├── JWThacker.py       # 主要逻辑：解码/编码接口
│   └── jwt_code.py        # JWT 核心操作类（Base64URL 编解码、签名验证）
└── README.md
```

---

## 快速开始

### 环境要求

- Python 3.10+

### 安装

```bash
# 克隆仓库
git clone https://github.com/Xiong-SJ/JWThacker.git
cd JWThacker

# 安装依赖
pip install -r requirements.txt
```

### 依赖说明

| 依赖 | 版本 | 用途 |
|------|------|------|
| [PyJWT](https://github.com/jpadilla/pyjwt) | 2.13.0 | JWT 编码与签名 |

---

## 使用示例

### 解码 JWT

```bash
python run.py decode "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzEyMyIsImV4cCI6MTc1MjU5MjAwMH0.abc123..."
```

输出：
```
{"alg":"HS256","typ":"JWT"}.{"sub":"user_123","exp":1752592000}.abc123...
```

### 编码（伪造）JWT

**完整格式**（Header + Payload 都以 JSON 字符串提供）：
```bash
python run.py encode '{"alg":"HS256","typ":"JWT"}.{"sub":"admin","exp":9999999999}' -p "my-secret-key"
```

**仅提供 Payload**（需指定算法）：
```bash
python run.py encode '{"sub":"admin","exp":9999999999}' --alg HS256 -p "my-secret-key"
```

**无密码签名（alg=none）**：
```bash
python run.py encode '{"alg":"none","typ":"JWT"}.{"sub":"admin"}'
python run.py encode '{"sub":"admin"}' --alg None
```

**签名密码爆破**
```bash
# 使用默认字典
python3 ./run.py brute eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiYWRtaW4ifQ.fXnqkrXQAP-LGQwu278ce7wMumjK5-BCGufrURKPSvE
# 使用指定字典
python3 ./run.py brute eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiYWRtaW4ifQ.fXnqkrXQAP-LGQwu278ce7wMumjK5-BCGufrURKPSvE -w PATH 

```

---

## 命令行参数

```
usage: run.py [-h] [--version] [-j JOBS] {decode,encode,brute} ...

positional arguments:
  {decode,encode,brute}
    decode              解码 JWT
    encode              编码 JWT
    brute               暴力破解 JWT 密码（还未开放）

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -j, --jobs JOBS       启用多进程加速（默认是4个进程）
```

---

## 开发计划

- [x] JWT 解码
- [x] JWT 编码（伪造）
- [x] 签名验证（`examine_jwt`）
- [x] 暴力破解（字典模式）
- [x] 启用多进程加速
- [X] 支持更多 JWT 算法（RS256, ES256 等）

---

## 注意事项

- 本工具仅供**安全研究、CTF 竞赛及授权测试**使用，请勿用于非法用途
- 使用 `alg=none` 攻击时，目标服务端需存在对应的算法混淆漏洞
- 暴力破解 HS256 等对称密钥时，建议使用强密码字典

---

## 作者

**YISHI(译世)**

**Benar**
