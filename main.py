import requests
import os
import shutil
import json
import time
import pystyle
from pystyle import Colorate, Colors
from Modules.gradients import gradient
from Modules.gradients import success, failure  
from Modules.spammer import send_webhook, spam_webhook_v2

class UtilityClonerMenu:
    def __init__(self):
        self.size = shutil.get_terminal_size().columns
        self.clear()
        self.render_ascii()
        self.main_menu()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_ascii(self):
        ascii_art = "\n".join([
            "   __  ____  _ ___ __       ______            __    _    _____      ",
            "  / / / / /_(_) (_) /___  _/_  __/___  ____  / /___| |  / /__ \\     ",
            " / / / / __/ / / / __/ / / // / / __ \\/ __ \\/ / ___/ | / /__/ /     ",
            "/ /_/ / /_/ / / / /_/ /_/ // / / /_/ / /_/ / (__  )| |/ // __/      ",
            "\\____/\\__/_/_/_/\\__/\\__, //_/  \\____/\\____/_/____/ |___//____/      ",
            "                   /____/                                           ",
            "",
            "                               [WebhookSpammer@UtilityToolsV2]                                          ",
            ""
        ])

        for line in ascii_art.splitlines():
            print(gradient(line.center(self.size)))

    def get_webhook_url(self):
        print("\n" + "═" * self.size)
        prompt_text = "[Webhook@UtilityToolsV2] Enter Webhook URL ~"
        print(gradient(prompt_text.center(self.size)))
        print("═" * self.size)
        
        webhook_url = input(Colorate.Horizontal(Colors.cyan_to_blue, "> ")).strip()
        
        while not webhook_url.startswith("https://discord.com/api/webhooks/"):
            print(failure(["[Webhook@UtilityToolsV2] Invalid Discord webhook URL format!"]))
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> "), end="")
            webhook_url = input().strip()
        
        return webhook_url

    def get_message_content(self):
        print("\n" + "═" * self.size)
        prompt_text = "[Webhook@UtilityToolsV2] Enter Message Content ~"
        print(gradient(prompt_text.center(self.size)))
        print("═" * self.size)
        print(Colorate.Horizontal(Colors.cyan_to_blue, "> "), end="")
        return input().strip()

    def get_thread_count(self):
        print("\n" + "═" * self.size)
        prompt_text = "[Webhook@UtilityToolsV2] Enter Number of Threads (1-100) ~"
        print(gradient(prompt_text.center(self.size)))
        print("═" * self.size)
        
        while True:
            try:
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> "), end="")
                count = int(input().strip())
                if 1 <= count <= 100:
                    return count
                else:
                    print(failure(["[Webhook@UtilityToolsV2] Please enter a number between 1 and 100"]))
            except ValueError:
                print(failure(["[Webhook@UtilityToolsV2] Please enter a valid number"]))

    def get_message_count(self):
        print("\n" + "═" * self.size)
        prompt_text = "[Webhook@UtilityToolsV2] Enter Total Messages to Send (0 for unlimited) "
        print(gradient(prompt_text.center(self.size)))
        print("═" * self.size)
        
        while True:
            try:
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> "), end="")
                count = int(input().strip())
                if count >= 0:
                    return count if count > 0 else None
                else:
                    print(failure(["[Webhook@UtilityToolsV2] Please enter a positive number or 0"]))
            except ValueError:
                print(failure(["[Webhook@UtilityToolsV2] Please enter a valid number"]))

    def get_delay(self):
        print("\n" + "═" * self.size)
        prompt_text = "[Webhook@UtilityToolsV2] Enter Delay Between Messages (0.5) "
        print(gradient(prompt_text.center(self.size)))
        print("═" * self.size)
        
        while True:
            try:
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> "), end="")
                delay = float(input().strip())
                if delay >= 0:
                    return delay
                else:
                    print(failure(["[Webhook@UtilityToolsV2] Please enter a positive number"]))
            except ValueError:
                print(failure(["[Webhook@UtilityToolsV2] Please enter a valid number"]))

    def show_config_summary(self, config):
        self.clear()
        self.render_ascii()
        
        print("\n" + "═" * self.size)
        print(gradient("[Webhook@UtilityToolsV2] Configuration Summary".center(self.size)))
        print("═" * self.size)
        
        summary = [
            f"Webhook URL: {config['webhook_url'][:50]}...",
            f"Message: {config['message'][:50]}...",
            f"Threads: {config['threads']}",
            f"Messages: {'Unlimited' if config['total_messages'] is None else config['total_messages']}",
            f"Delay: {config['delay']} seconds",
        ]
        
        for item in summary:
            print(Colorate.Horizontal(Colors.cyan_to_blue, f"  {item}"))
        
        print("\n" + "═" * self.size)
        confirm_prompt = "[Webhook@UtilityToolsV2] Press Enter to Start Spamming (Ctrl+C to Cancel) ~"
        print(gradient(confirm_prompt.center(self.size)))
        print("═" * self.size)
        input(Colorate.Horizontal(Colors.cyan_to_blue, "> "))

    def main_menu(self):
        webhook_url = self.get_webhook_url()        
        self.clear()
        self.render_ascii()
        message = self.get_message_content()
        self.clear()
        self.render_ascii()
        threads = self.get_thread_count()
        self.clear()
        self.render_ascii()
        total_messages = self.get_message_count()
        self.clear()
        self.render_ascii()        
        delay = self.get_delay()        
        config = {
            'webhook_url': webhook_url,
            'message': message,
            'threads': threads,
            'total_messages': total_messages,
            'delay': delay
        }        
        self.show_config_summary(config)        
        self.clear()
        self.render_ascii()
        print("\n" + "═" * self.size)
        print(gradient("[Webhook@UtilityToolsV2] Starting Spam ".center(self.size)))
        print("═" * self.size)
        
        try:
            spam_webhook_v2(
                webhook_url=config['webhook_url'],
                content=config['message'],
                thread_count=config['threads'],
                total_messages=config['total_messages'],
                delay=config['delay']
            )
            
            print("\n" + "═" * self.size)
            print(gradient("[Webhook@UtilityToolsV2] Attack Completed!".center(self.size)))
            print("═" * self.size)
            
        except KeyboardInterrupt:
            print("\n" + "═" * self.size)
            print(failure(["[Webhook@UtilityToolsV2] Attack Stopped by User!"]))
            print("═" * self.size)
        except Exception as e:
            print("\n" + "═" * self.size)
            print(failure([f"[Webhook@UtilityToolsV2] Error: {e}"]))
            print("═" * self.size)
        
        print("\n" + "═" * self.size)
        restart_prompt = "[Webhook@UtilityToolsV2] Run Again? (y/n) ~"
        print(gradient(restart_prompt.center(self.size)))
        print("═" * self.size)
        print(Colorate.Horizontal(Colors.cyan_to_blue, "> "), end="")
        
        choice = input().strip().lower()
        if choice == 'y':
            self.clear()
            UtilityClonerMenu()
        else:
            print("\n" + gradient("[Webhook@UtilityToolsV2] Goodbye!".center(self.size)))
            exit()

if __name__ == "__main__":
    UtilityClonerMenu()