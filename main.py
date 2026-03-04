import os
import shutil
import sys
import time
from pystyle import Colorate, Colors
from Modules.gradients import gradient, success, failure
from Modules.utils import ensure

ensure()

class MainHub:
    def __init__(self):
        self.size = shutil.get_terminal_size().columns
        self.clear()
        self.render_ascii()
        self.show_options()

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
                               [MainHub@UtilityToolsV2]
        """
        for line in ascii_art.splitlines():
            print(gradient(line.center(self.size)))

    def show_options(self):
        print("\n" + "═" * self.size)
        print(gradient("Select a Utility to Launch".center(self.size)))
        print("═" * self.size + "\n")

        options = [
            "[1] Webhook Spammer",
            "[2] Webhook Deleter",
            "[3] Exit Program"
        ]

        for opt in options:
            print(gradient(f"      {opt}"))

        print("\n" + "═" * self.size)
        choice = input(Colorate.Horizontal(Colors.cyan_to_blue, "Choice > ")).strip()

        if choice == '1':
            self.launch_tool("spammer")
        elif choice == '2':
            self.launch_tool("deleter")
        elif choice == '3':
            print(gradient("\n[!] Shutting down...".center(self.size)))
            sys.exit()
        else:
            print(failure("[!] Invalid Selection!"))
            time.sleep(1)
            self.__init__()

    def launch_tool(self, tool_name):
        try:
            if tool_name == "spammer":
                from Modules.spammer import UtilityClonerMenu
                UtilityClonerMenu()
            elif tool_name == "deleter":
                from Modules.deleter import WebhookDeleterMenu
                WebhookDeleterMenu()
        except ImportError as e:
            print(failure(f"[!] {tool_name}.py not found or import error: {e}"))
            input("\nPress Enter to return to menu...")
            self.__init__()
        except Exception as e:
            print(failure(f"[!] Error launching {tool_name}: {e}"))
            input("\nPress Enter to return to menu...")
            self.__init__()

if __name__ == "__main__":
    try:
        MainHub()
    except KeyboardInterrupt:
        print(failure("\n\n[!] Session Terminated."))
        sys.exit()
