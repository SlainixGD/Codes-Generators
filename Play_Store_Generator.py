import time
import requests
import random
import string
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor

init()  # Initialize colorama

class PlayStoreCodeGenerator:
    def __init__(self):
        self.codes_generated = set()  # Use a set to avoid duplicate codes

    def generate_code(self):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        while code in self.codes_generated:  # Ensure the generated code is unique
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        self.codes_generated.add(code)
        return code

    def is_valid_code(self, code):
        url = f"https://play.google.com/store/apps/details?id={code}"
        response = requests.get(url)
        return response.status_code == 200

    def save_code_to_file(self, code, validity):
        file_name = "valid_play_store_codes.txt" if validity else "invalid_play_store_codes.txt"
        with open(file_name, "a") as file:
            file.write(code + "\n")

    def generate_and_check_code(self):
        while True:
            code = self.generate_code()
            validity = self.is_valid_code(code)
            self.save_code_to_file(code, validity)
            if validity:
                print(f"{Fore.GREEN}[VALID]{Style.RESET_ALL} {code}")
            else:
                print(f"{Fore.RED}[INVALID]{Style.RESET_ALL} {code}")
            time.sleep(0.01)  # Sleep for 10 milliseconds

    def start(self, num_threads=5):
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for _ in range(num_threads):
                executor.submit(self.generate_and_check_code)

if __name__ == "__main__":
    generator = PlayStoreCodeGenerator()
    generator.start()
