import requests
import os
import shutil
import time
from pystyle import Colorate, Colors
from Modules.gradients import gradient, success, failure  
from Modules.utils import ensure

class WebhookDeleterMenu:
    def __init__(self):
        self.size = shutil.get_terminal_size().columns
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
                               [WebhookDeleter@UtilityToolsV2]
        """
        for line in ascii_art.splitlines():
            print(gradient(line.center(self.size)))

    def delete_webhook(self, url):
        print(gradient(f"\n[*] Attempting to delete: {url[:50]}..."))
        try:
            check = requests.get(url)
            if check.status_code == 404:
                print(failure("[!] Webhook already deleted or invalid!"))
                return
            
            response = requests.delete(url)
            if response.status_code == 204:
                print(success("[+] Webhook successfully deleted!"))
            elif response.status_code == 429:
                print(failure("[!] Rate limited. Please wait a moment."))
            else:
                print(failure(f"[!] Failed to delete. Status: {response.status_code}"))
        
        except Exception as e:
            print(failure(f"[!] An error occurred: {e}"))

    def run_logic(self):
        while True:
            url = input(gradient("\n[>] Enter Webhook URL to Delete: ")).strip()
            if url.startswith("https://discord.com/api/webhooks/"):
                break
            print(failure("[!] Invalid Discord Webhook format!"))
        
        print("\n" + "═" * self.size)
        confirm = input(gradient("[?] Are you sure you want to delete this? (y/n): ")).strip().lower()
        
        if confirm == 'y':
            self.delete_webhook(url)
        else:
            print(gradient("\n[!] Deletion cancelled."))
        
        print("\n" + "═" * self.size)
        print(gradient("Press Enter to Return to Menu".center(self.size)))
        input()

if __name__ == "__main__":
    ensure() 
    try:
        WebhookDeleterMenu()
    except KeyboardInterrupt:
        print(failure("\n[!] Exiting..."))