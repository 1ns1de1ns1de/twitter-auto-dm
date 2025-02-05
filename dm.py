import csv
import os
import time
import random
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# Install ChromeDriver if needed
chromedriver_autoinstaller.install()

# Folders and Files
COOKIES_FOLDER = 'cookies'
DATA_FILE = 'data.txt'
MESSAGE_FILE = 'message.txt'
CSV_LOG_FILE = 'dm_log.csv'

# Global variable declaration at the top of the script
global default_delay_range
default_delay_range = (10, 40)  # Changed to shorter default delay

# Function to read usernames from a file
def read_usernames(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"File {file_path} not found.")
        return []

# Function to read usernames and messages from a file
def read_usernames_and_messages(data_file, message_file):
    try:
        # Baca daftar username
        with open(data_file, 'r', encoding='utf-8') as data:
            usernames = [line.strip() for line in data if line.strip()]
        
        # Baca pesan dari file pesan
        with open(message_file, 'r', encoding='utf-8') as msg:
            messages = [line.strip() for line in msg if line.strip()]
        
        # Jika jumlah pesan kurang dari username, gunakan pesan berulang
        if len(messages) < len(usernames):
            messages = messages * (len(usernames) // len(messages) + 1)
        
        # Pasangkan username dengan pesan
        return list(zip(usernames, messages[:len(usernames)]))
    
    except FileNotFoundError as e:
        print(Fore.RED + f"File not found: {e}")
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

# Function to load cookies with increased wait time
def load_cookies(driver, account_name):
    cookies_file = os.path.join(COOKIES_FOLDER, f"twitter_{account_name}.pkl")
    if os.path.exists(cookies_file):
        with open(cookies_file, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print(Fore.GREEN + f"Cookies loaded for Twitter account {account_name}.")
        time.sleep(5)  # Added delay after loading cookies
    else:
        print(Fore.YELLOW + f"Cookies not found for Twitter account {account_name}. Manual login required.")

# Function to save cookies
def save_cookies(driver, account_name):
    cookies = driver.get_cookies()
    cookies_file = os.path.join(COOKIES_FOLDER, f"twitter_{account_name}.pkl")
    with open(cookies_file, 'wb') as file:
        pickle.dump(cookies, file)
    print(Fore.GREEN + f"Cookies saved for Twitter account {account_name}.")

# Initialize Chrome Driver with options
def init_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    return webdriver.Chrome(options=chrome_options)

# Function to update delay range
def update_delay_settings():
    global default_delay_range  # Add global declaration at the top of the function
    try:
        print(Fore.CYAN + "\nCurrent delay range:", default_delay_range)
        min_delay = int(input(Fore.LIGHTYELLOW_EX + "Enter minimum delay (in seconds): "))
        max_delay = int(input(Fore.LIGHTYELLOW_EX + "Enter maximum delay (in seconds): "))
        
        if min_delay > 0 and max_delay > min_delay:
            default_delay_range = (min_delay, max_delay)
            print(Fore.GREEN + f"Delay range updated to: {default_delay_range} seconds")
        else:
            print(Fore.RED + "Invalid input. Max delay must be greater than min delay and both must be positive.")
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter numbers only.")

# Start Selenium with cookies
def start_selenium():
    account_name = input(Fore.LIGHTYELLOW_EX + "Enter Twitter account name: ").strip()
    driver = init_chrome_driver()
    
    driver.get("https://twitter.com/login")
    time.sleep(5)  # Added delay before loading cookies
    load_cookies(driver, account_name)
    
    if not any(cookie['name'] == 'auth_token' for cookie in driver.get_cookies()):
        print(Fore.LIGHTYELLOW_EX + "Manual login required.")
        input(Fore.LIGHTMAGENTA_EX + "Press Enter after logging in...")
        save_cookies(driver, account_name)

    print(Fore.GREEN + f"Selenium ready for Twitter account {account_name}.")
    driver.quit()

# Start Auto DM Twitter
def start_auto_dm():
    global default_delay_range
    account_name = input(Fore.LIGHTYELLOW_EX + "Enter Twitter account name: ").strip()
    driver = init_chrome_driver()

    driver.get("https://twitter.com/login")
    time.sleep(5)  # Added delay before loading cookies
    load_cookies(driver, account_name)

    if not any(cookie['name'] == 'auth_token' for cookie in driver.get_cookies()):
        print(Fore.LIGHTYELLOW_EX + "Manual login required.")
        input(Fore.LIGHTMAGENTA_EX + "Press Enter after logging in...")
        save_cookies(driver, account_name)

    # Gunakan fungsi baru untuk membaca username dan pesan
    user_messages = read_usernames_and_messages(DATA_FILE, MESSAGE_FILE)

    if not user_messages:
        print(Fore.LIGHTRED_EX + "Username list or message list is empty. Script stopped.")
        driver.quit()
        return

    print(Fore.CYAN + f"Starting to send DMs with delay range: {default_delay_range[0]}-{default_delay_range[1]} seconds")
    
    for username, message in tqdm(user_messages, desc="Sending DMs", unit="user"):
        status = send_dm(driver, username, message, debug=False)
        log_dm_result(CSV_LOG_FILE, username, status)

        delay = random.randint(*default_delay_range)
        print(Fore.LIGHTMAGENTA_EX + f"Waiting for {delay} seconds before next DM...")
        time.sleep(delay)

    print(Fore.GREEN + "\nDM sending process completed!")
    driver.quit()

# Main menu
def main_menu():
    print(Fore.MAGENTA + """
        #######################################
        #                                     #
        #          1ns1de Auto DM Bot         #
        #                                     #
        #######################################
    """ + Style.RESET_ALL)

    while True:
        print(Fore.LIGHTMAGENTA_EX + "\nChoose an option:")
        print(Fore.LIGHTCYAN_EX + "1. Start Selenium (manual login and save cookies)")
        print(Fore.LIGHTCYAN_EX + "2. Start Auto DM Twitter")
        print(Fore.LIGHTCYAN_EX + "3. Update Delay Settings")
        print(Fore.LIGHTCYAN_EX + "4. Exit")
        choice = input(Fore.LIGHTYELLOW_EX + "Enter your choice (1/2/3/4): ")

        if choice == '1':
            start_selenium()
        elif choice == '2':
            start_auto_dm()
        elif choice == '3':
            update_delay_settings()
        elif choice == '4':
            print(Fore.LIGHTRED_EX + "Exiting the program.")
            break
        else:
            print(Fore.LIGHTRED_EX + "Invalid choice. Please try again.")

if __name__ == "__main__":
    # Create cookies folder if it doesn't exist
    if not os.path.exists(COOKIES_FOLDER):
        os.makedirs(COOKIES_FOLDER)
    main_menu()
