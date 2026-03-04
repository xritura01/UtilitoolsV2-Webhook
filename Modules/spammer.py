import requests
import os
import shutil
import json
import time
from pystyle import Colorate, Colors
from Modules.gradients import gradient, success, failure  
from Modules.function import spam_webhook_v2
from Modules.utils import ensure, proxy_loader, Forwarder_loader

ensure()  

class UtilityClonerMenu:
    def __init__(self):
        self.size = shutil.get_terminal_size().columns
        self.UsingProxy = False
        self.ProxyMethod = None
        
        self.clear()
        self.render_ascii()
        self.run_logic()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_ascii(self):
        ascii_art = r"""
   __  ____  _ ___ __       ______            __    _    _____      
  / / / / /_(_) (_) /___  _/_  __/___  ____  / /___| |  / /__ \     
 / / / / __/ / / / __/ / / // / / __ \/ __ \/ / ___/ | / /__/ /     
/ /_/ / /_/ / / / /_/ /_/ // / / /_/ / /_/ / (__  )| |/ // __/      
\____/\__/_/_/_/\__/ \__, //_/  \____/\____/_/____/ |___//____/      
                    /____/                                           
                               [WebhookSpammer@UtilityToolsV2]
        """
        for line in ascii_art.splitlines():
            print(gradient(line.center(self.size)))

    def setup_proxy(self):
        prompt_text = "\n[?] Use a proxy? (y/n) ~ "
        choice = input(gradient(prompt_text)).strip().lower()
        
        if choice == 'y':
            if not os.path.exists("data/proxies.txt"):
                print(failure("[!] data/proxies.txt not found!"))
                return False
            
            with open("data/proxies.txt", "r") as f:
                if not f.read().strip():
                    print(failure("[!] No proxies found in proxies.txt!"))
                    return False
            
            self.UsingProxy = True
            print(gradient("1 ~> Forwarder | 2 ~> HTTP | 3 ~> SOCKS5"))
            p_choice = input(Colorate.Horizontal(Colors.cyan_to_blue, "Method > ")).strip()
            mapping = {"1": "forwarder", "2": "http", "3": "socks5"}
            self.ProxyMethod = mapping.get(p_choice, "http")
            return True
        return False

    def get_inputs(self):
        while True:
            url = input(gradient("[>] Webhook URL: ")).strip()
            if self.UsingProxy or url.startswith("https://discord.com/api/webhooks/"):
                webhook_url = url
                break
            print(failure("[!] Invalid Discord Webhook format!"))

        message = input(gradient("[>] Message Content: ")).strip()
        while True:
            try:
                threads = int(input(gradient("[>] Threads (1-6): ")).strip())
                if 1 <= threads <= 6: break
                print(failure("[!] Please keep threads between 1 and 6."))
            except ValueError: print(failure("[!] Enter a valid number."))

        while True:
            try:
                count_raw = input(gradient("[>] Total Messages (0 for unlimited): ")).strip()
                count = int(count_raw) if count_raw else 0
                total_messages = count if count > 0 else None
                break
            except ValueError: print(failure("[!] Enter a valid number."))

        while True:
            try:
                delay_raw = input(gradient("[>] Delay (e.g. 0.5): ")).strip()
                delay = float(delay_raw) if delay_raw else 0.5
                break
            except ValueError: print(failure("[!] Enter a valid number."))

        return {
            'webhook_url': webhook_url,
            'message': message,
            'threads': threads,
            'total_messages': total_messages,
            'delay': delay
        }

    def run_logic(self):
        self.setup_proxy()
        config = self.get_inputs()
        print(gradient(f"[*] Starting Spammer on {config['webhook_url'][:40]}...".center(self.size)))
        print(gradient("[!] Press CTRL+C to stop anytime".center(self.size)))
        print("═" * self.size + "\n")

        try:
            spam_webhook_v2(
                webhook_url=config['webhook_url'],
                content=config['message'],
                thread_count=config['threads'],
                total_messages=config['total_messages'],
                delay=config['delay'],
                proxies=self.UsingProxy,
                proxy_method=self.ProxyMethod
            )
            print(success("\n[+] Task Completed Successfully."))
        except KeyboardInterrupt:
            print(failure("\n[!] Stopped by User."))
        except Exception as e:
            print(failure(f"\n[!] Error: {e}"))

if __name__ == "__main__":
    UtilityClonerMenu()