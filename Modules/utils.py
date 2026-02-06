import os 
def proxy_loader():
    try:
        with open("data/proxies.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []
