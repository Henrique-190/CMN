import colorama
import datetime

from colorama import Fore, Style

colorama.init(autoreset=True)


class ColoredLogger:
    COLORS = {
        'DBG': Fore.BLUE,
        'INF': Fore.GREEN,
        'SUC': f'{Fore.GREEN}{Style.BRIGHT}',
        'WRN': Fore.YELLOW,
        'ERR': Fore.RED,
        'CRI': f'{Fore.RED}{Style.BRIGHT}',
    }

    def __init__(self, debug_enabled: bool = False):
        self.debug_enabled = debug_enabled

    def log(self, level, msg):
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
              f"{self.COLORS.get(level)}{level}{Fore.RESET}{Style.RESET_ALL} - "
              f"{msg}")

    def debug(self, msg):
        if self.debug_enabled:
            self.log('DBG', msg)

    def info(self, msg):
        if self.debug_enabled:
            self.log('INF', msg)

    def success(self, msg):
        self.log('SUC', msg)

    def warning(self, msg):
        self.log('WRN', msg)

    def error(self, msg):
        self.log('ERR', msg)

    def critical(self, msg):
        self.log('CRI', msg)
