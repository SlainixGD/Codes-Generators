import time
import requests
import random
import string
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor

init()  # Initialize colorama

class SteamKeyGenerator:
    def __init__(self):
        self.keys_generated = set()  # Use a set to avoid duplicate keys

    def generate_key(self):
        key = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) for _ in range(5)])
        while key in self.keys_generated:  # Ensure the generated key is unique
            key = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) for _ in range(5)])
        self.keys_generated.add(key)
        return key

    def is_valid_key(self, key):
        url = f"https://api.steampowered.com/ISteamUserAuth/AuthenticateUser/v0001/?key={key}"
        response = requests.get(url)
        return response.status_code == 200

    def save_key_to_file(self, key, validity):
        file_name = "valid_steam_codes.txt" if validity else "invalid_steam_codes.txt"
        with open(file_name, "a") as file:
            file.write(key + "\n")

    def generate_and_check_key(self):
        while True:
            key = self.generate_key()
            validity = self.is_valid_key(key)
            self.save_key_to_file(key, validity)
            if validity:
                print(f"{Fore.GREEN}[VALID]{Style.RESET_ALL} {key}")
            else:
                print(f"{Fore.RED}[INVALID]{Style.RESET_ALL} {key}")
            time.sleep(0.01)  # Sleep for 10 milliseconds

    def start(self, num_threads=5):
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for _ in range(num_threads):
                executor.submit(self.generate_and_check_key)

if __name__ == "__main__":
    generator = SteamKeyGenerator()
    generator.start()
