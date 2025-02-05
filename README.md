# Auto DM Twitter Bot

## Overview
This script automates sending Direct Messages (DM) on Twitter using Selenium. It supports multiple users, reads usernames and messages from text files, and logs the DM status in a CSV file. The bot also supports cookie-based login to avoid repeated manual authentication.

## Features
- **Automatic DM sending**: Reads usernames and messages from files and sends DMs.
- **Cookie-based login**: Saves and loads login cookies to avoid manual authentication.
- **Custom delay settings**: Allows setting custom delays between messages to avoid detection.
- **Logs message status**: Saves sent message statuses in a CSV file.
- **Manual login option**: Allows manual login if cookies are not available.
- **Error handling**: Handles missing files and failed DM attempts gracefully.
- **Automatic folder creation**: Ensures required directories (e.g., `cookies/`) are created if missing.

## Prerequisites
### Install Dependencies
Ensure you have Python installed (Python 3.x recommended). Install the required dependencies using:
```sh
pip install selenium chromedriver-autoinstaller tqdm colorama
```

### Install ChromeDriver
This script automatically installs the required ChromeDriver version using `chromedriver-autoinstaller`.

## Setup Instructions
### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/auto-dm-twitter.git
cd auto-dm-twitter
```

### 2. Setup Twitter Login
Before running the bot, you need to log in and save cookies:
```sh
python dm.py
```
Select option **1. Start Selenium (manual login and save cookies)** and log in manually. The bot will save cookies for future logins.

### 3. Prepare User Data
Create the following files in the script directory:
- `data.txt`: Contains Twitter usernames (one per line).
- `message.txt`: Contains messages (one per line). If there are fewer messages than usernames, messages will repeat.

Example `data.txt`:
```
user1
user2
user3
```

Example `message.txt`:
```
Hello! How are you?
This is an automated message.
```

### 4. Start Auto DM
Run the script and select option **2. Start Auto DM Twitter**:
```sh
python dm.py
```
The bot will send messages with random delays.

### 5. Adjust Delay Settings (Optional)
You can customize the delay between messages by selecting **3. Update Delay Settings**.

## Output Files
- **`dm_log.csv`**: Logs the status of each sent DM.
  - Format: `Username, Status`
  - Example:
    ```csv
    Username,Status
    user1,Sent
    user2,Failed to send DM
    ```
- **Cookies (`cookies/twitter_<account>.pkl`)**: Stores session cookies for automatic login.

## Automatic Folder Creation
The script ensures that the necessary folders are created automatically. If the `cookies` folder does not exist, it will be created at runtime:
```python
if not os.path.exists(COOKIES_FOLDER):
    os.makedirs(COOKIES_FOLDER)
```
This ensures smooth execution without requiring manual folder creation.

## Error Handling
- If the script cannot find `data.txt` or `message.txt`, it will display an error message.
- If a DM fails to send, it will log the failure in `dm_log.csv`.
- If login cookies are missing, the script will prompt manual login.

## Notes
- Ensure Chrome is installed and updated.
- Use this bot responsibly to comply with Twitter's policies.
- This script does **not** bypass Twitter's DM limits or restrictions.

## Contributing
Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This script is provided "as is" without warranty of any kind. Use at your own risk.

## Author
[Your Name]

## Support
If you encounter any issues, feel free to open an issue on [GitHub](https://github.com/yourusername/auto-dm-twitter/issues).

## Like this project?
If you find this project helpful, please consider giving it a ⭐ on [GitHub](https://github.com/yourusername/auto-dm-twitter)!

