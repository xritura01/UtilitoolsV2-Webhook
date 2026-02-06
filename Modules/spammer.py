import os 
import requests
import random
import threading
import time
from pystyle import Colorate, Colors
from Modules.utils import proxy_loader
from Modules.gradients import success, failure

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0'
]

def send_webhook(webhook_url, content, delay=0.5):
    proxies_list = proxy_loader()
    
    proxies = None
    if proxies_list:
        proxy = random.choice(proxies_list)
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    
    payload = {"content": content}
    
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            proxies=proxies,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 204:
            print(success(f"[Webhook@UtilityToolsV2] Message sent successfully!"))
        else:
            print(failure(f"[Webhook@UtilityToolsV2] Failed to send message. Status Code: {response.status_code}"))
            
    except requests.exceptions.RequestException as e:
        print(failure(f"[Webhook@UtilityToolsV2] Error: {e}"))

    time.sleep(delay)

def spam_webhook(webhook_url, content, thread_count, message_count=None, delay=0.5):
    def worker():
        if message_count:
            for i in range(message_count):
                send_webhook(webhook_url, content, delay)
        else:
            message_counter = 0
            while True:
                message_counter += 1
                send_webhook(webhook_url, content, delay)
    
    threads = []
    for i in range(thread_count):
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        threads.append(thread)
        print(success(f"[Webhook@UtilityToolsV2] Started thread {i+1}/{thread_count}"))
    if message_count:
        for thread in threads:
            thread.join()
    else:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(failure(f"[Webhook@UtilityToolsV2] Stopping all threads..."))

def spam_webhook_v2(webhook_url, content, thread_count, total_messages=None, delay=0.5):
    message_counter = 0
    stop_flag = threading.Event()
    
    def worker():
        nonlocal message_counter
        while not stop_flag.is_set():
            if total_messages and message_counter >= total_messages:
                break
                
            with threading.Lock():
                if total_messages and message_counter >= total_messages:
                    break
                current_msg = message_counter + 1
                message_counter += 1
            
            print(success(f"[Webhook@UtilityToolsV2] Thread {threading.current_thread().name}: Sending message #{current_msg}"))
            
            send_webhook(webhook_url, content, delay)
    
    threads = []
    for i in range(thread_count):
        thread = threading.Thread(target=worker, name=f"Thread-{i+1}")
        thread.start()
        threads.append(thread)
        print(success(f"[Webhook@UtilityToolsV2] Started thread {i+1}/{thread_count}"))
    
    try:
        if total_messages:
            while message_counter < total_messages:
                time.sleep(0.1)
            stop_flag.set()
        for thread in threads:
            thread.join(timeout=1)
            
    except KeyboardInterrupt:
        print(failure(f"[Webhook@UtilityToolsV2] Stopping all threads..."))
        stop_flag.set()
        for thread in threads:
            thread.join(timeout=2)
    
    print(success(f"[Webhook@UtilityToolsV2] Completed! Total messages sent: {message_counter}"))
