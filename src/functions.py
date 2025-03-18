# functions.py :]
import requests
import threading
import time
import random
from typing import List
from colorama import Fore, Style

def log(status: str, message: str) -> None:
    color = Fore.GREEN if status == "OK" else Fore.RED
    print(f"{color}[{status}]{Style.RESET_ALL} {message}")

class Functions:
    session = requests.Session()

    @staticmethod
    def request(post_id: int, direction: str, proxy: str) -> bool:
        try:
            response = Functions.session.post(
                "https://api.urbandictionary.com/v0/vote",
                json={"defid": post_id, "direction": direction},
                headers={"Content-Type": "application/json"},
                proxies={"http": proxy, "https": proxy},
                timeout=3
            )
            log("OK", f"Response: {response.status_code} | Proxy: {proxy}")
            return response.status_code == 200
        except requests.RequestException:
            from main import ERR_PRINT_ENABLED
            if ERR_PRINT_ENABLED:
                log("ERR", f"Failed request with proxy: {proxy}")
            return False

    @staticmethod
    def load_proxies(filename: str = "proxies.txt") -> List[str]:
        try:
            with open(filename, "r") as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            log("ERR", "proxies.txt not found.")
            return []

    @staticmethod
    def filter_working_proxies(proxies: List[str]) -> List[str]:
        working_proxies: List[str] = []
        proxy_lock = threading.Lock()

        def test_proxy(proxy: str):
            if Functions.request(12417197, "up", proxy):
                with proxy_lock:
                    working_proxies.append(proxy)

        threads = [threading.Thread(target=test_proxy, args=(proxy,)) for proxy in proxies]
        for thread in threads: thread.start()
        for thread in threads: thread.join()

        # log("OK", f"Working proxies: {len(working_proxies)}/{len(proxies)}")               <-- this one is being weird idk why
        return working_proxies

    @staticmethod
    def begin(post_id: int, direction: str) -> None:
        if direction not in {"up", "down"}:
            raise ValueError("Direction must be 'up' or 'down'.")

        proxies = Functions.filter_working_proxies(Functions.load_proxies())
        if not proxies:
            log("ERR", "No working proxies found. Exiting...")
            return

        proxy_lock = threading.Lock()
        proxy_queue = proxies[:]

        def worker():
            while True:
                with proxy_lock:
                    if not proxy_queue:
                        break
                    proxy = proxy_queue.pop(0)
                if Functions.request(post_id, direction, proxy):
                    time.sleep(random.uniform(0.5, 1))

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for thread in threads: thread.start()
        for thread in threads: thread.join()
