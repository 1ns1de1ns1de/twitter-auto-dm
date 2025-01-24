import csv
import os
import time
import random
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# Cookies folder
COOKIES_FOLDER = 'cookies'

# File Paths
DATA_FILE = 'data.txt'
MESSAGE_FILE = 'message.txt'
CSV_LOG_FILE = 'dm_log.csv'

# Delay Configuration
default_delay_range = (120, 180)

# Function to read usernames from a file
def read_usernames(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"File {file_path} not found.")
        return []

# Function to read the message from a file
def read_message(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(Fore.RED + f"File {file_path} not found.")
        return ""

# Function to log DM results to a CSV file
def log_dm_result(csv_file, username, status):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Username', 'Status'])  # Header
        writer.writerow([username, status])  # Log data

# Function to send a DM using Selenium
def send_dm(driver, username, message, debug=False):
    try:
        driver.get(f"https://twitter.com/{username}")
        time.sleep(3)

        try:
            xpath_options = [
                "//div[@data-testid='sendDMFromProfile']",
                "//button[@data-testid='sendDMFromProfile']",
                "//div[@role='button' and @aria-label='Message']",
            ]
            message_button = None
            for xpath in xpath_options:
                try:
                    message_button = driver.find_element(By.XPATH, xpath)
                    if message_button.is_displayed():
                        break
                except:
                    continue

            if not message_button:
                print(Fore.YELLOW + f"'Message' button not found for {username}.")
                return "Failed to send DM"

            message_button.click()
        except Exception as e:
            print(Fore.RED + f"'Message' button not found for {username}: {e}")
            return "Failed to send DM"

        try:
            message_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-offset-key and contains(@class, 'public-DraftStyleDefault-block')]"))
            )
            message_input.click()
            message_input.send_keys(message)
            time.sleep(1)
            message_input.send_keys(Keys.ENTER)
        except Exception as e:
            print(Fore.RED + f"Message input area not found: {e}")
            return "Failed to send DM"

        print(Fore.GREEN + f"DM sent to {username}")
        return "Sent"
    except Exception as e:
        if debug:
            print(Fore.RED + f"Error sending DM to {username}: {e}")
        return "Error"

# Function to load cookies
def load_cookies(driver, account_type, account_name):
    cookies_file = os.path.join(COOKIES_FOLDER, f"{account_type}_{account_name}.pkl")
    if os.path.exists(cookies_file):
        with open(cookies_file, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print(Fore.GREEN + f"Cookies loaded for {account_type} account {account_name}.")
    else:
        print(Fore.YELLOW + f"Cookies not found for {account_type} account {account_name}. Manual login required.")

# Function to save cookies
def save_cookies(driver, account_type, account_name):
    cookies = driver.get_cookies()
    cookies_file = os.path.join(COOKIES_FOLDER, f"{account_type}_{account_name}.pkl")
    with open(cookies_file, 'wb') as file:
        pickle.dump(cookies, file)
    print(Fore.GREEN + f"Cookies saved for {account_type} account {account_name}.")

# Main menu
def main_menu():
    print(Fore.MAGENTA + """
        #######################################
        #                                     #
        #          1ns1de Auto DM Bot        #
        #                                     #
        #######################################
    """ + Style.RESET_ALL)

    while True:
        print(Fore.LIGHTMAGENTA_EX + "\nChoose an option:")
        print(Fore.LIGHTCYAN_EX + "1. Start Selenium (manual login and save cookies)")
        print(Fore.LIGHTCYAN_EX + "2. Start Auto DM Twitter")
        print(Fore.LIGHTCYAN_EX + "3. Exit")
        choice = input(Fore.LIGHTYELLOW_EX + "Enter your choice (1/2/3): ")

        if choice == '1':
            start_selenium()
        elif choice == '2':
            start_auto_dm()
        elif choice == '3':
            print(Fore.LIGHTRED_EX + "Exiting the program.")
            break
        else:
            print(Fore.LIGHTRED_EX + "Invalid choice. Please try again.")

# Start Selenium with or without cookies
def start_selenium():
    account_type = input(Fore.LIGHTYELLOW_EX + "Enter account type (twitter/gmail): ").strip().lower()
    account_name = input(Fore.LIGHTYELLOW_EX + "Enter account name: ").strip()

    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    if account_type == 'twitter':
        driver.get("https://twitter.com/login")
        load_cookies(driver, account_type, account_name)
        if not any(cookie['name'] == 'auth_token' for cookie in driver.get_cookies()):
            print(Fore.LIGHTYELLOW_EX + "Manual login required.")
            input(Fore.LIGHTMAGENTA_EX + "Press Enter after logging in...")
            save_cookies(driver, account_type, account_name)
    elif account_type == 'gmail':
        driver.get("https://mail.google.com")
        load_cookies(driver, account_type, account_name)
        if not any(cookie['name'] == 'G_AUTHUSER_H' for cookie in driver.get_cookies()):
            print(Fore.LIGHTYELLOW_EX + "Manual login required.")
            input(Fore.LIGHTMAGENTA_EX + "Press Enter after logging in...")
            save_cookies(driver, account_type, account_name)

    print(Fore.GREEN + f"Selenium ready for {account_type} account {account_name}.")
    driver.quit()

# Start Auto DM Twitter
def start_auto_dm():
    account_name = input(Fore.LIGHTYELLOW_EX + "Enter Twitter account name: ").strip()

    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    driver.get("https://twitter.com/login")
    load_cookies(driver, 'twitter', account_name)

    if not any(cookie['name'] == 'auth_token' for cookie in driver.get_cookies()):
        print(Fore.LIGHTYELLOW_EX + "Manual login required.")
        input(Fore.LIGHTMAGENTA_EX + "Press Enter after logging in...")
        save_cookies(driver, 'twitter', account_name)

    usernames = read_usernames(DATA_FILE)
    message = read_message(MESSAGE_FILE)

    if not usernames or not message:
        print(Fore.LIGHTRED_EX + "Username list or message is empty. Script stopped.")
        driver.quit()
        return

    start_time = time.time()
    for username in tqdm(usernames, desc="Sending DMs", unit="user"):
        if time.time() - start_time > 8 * 60 * 60:
            print(Fore.LIGHTYELLOW_EX + "8-hour limit reached. Stopping the script.")
            break

        status = send_dm(driver, username, message, debug=False)
        log_dm_result(CSV_LOG_FILE, username, status)

        delay = random.randint(*default_delay_range)
        print(Fore.LIGHTMAGENTA_EX + f"Waiting for {delay} seconds before continuing...")
        time.sleep(delay)

    driver.quit()

if __name__ == "__main__":
    main_menu()
