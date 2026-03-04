import os 
def proxy_loader():
    try:
        with open("data/proxies.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def ensure():
    if not os.path.exists("data"):
        os.makedirs("data")
    for filename in ["proxies.txt", "forwarder.txt"]:
        filepath = os.path.join("data", filename)
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                pass

def Forwarder_loader():
    try:
        with open("data/forwarder.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []
