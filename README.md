# Auto DM Twitter Bot

This repository contains a Python script designed to automate the process of sending direct messages (DMs) on Twitter using Selenium. The bot supports cookie management, dynamic message sending, and CSV logging for DM statuses.

## Features

- **Automated DM Sending**: Automatically sends DMs to a list of Twitter usernames.
- **Cookie Management**: Saves and loads cookies to avoid repeated logins.
- **Dynamic Message Input**: Reads custom messages from a text file.
- **CSV Logging**: Logs the DM results in a CSV file for easy tracking.

## Requierments
* Python 3.8 or higher
* Google Chrome
* ChromeDriver
* Required Python libraries:
  - selenium
  - webdriver-manager
  - tqdm
  - colorama

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/twitter-auto-dm.git
   cd twitter-auto-dm
   ```

2. Install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure that Google Chrome and ChromeDriver are installed and compatible with your system.

## Usage

1. **Prepare Your Data**:

   - Create a `data.txt` file containing the list of Twitter usernames (one username per line).
   - Create a `message.txt` file with the message you want to send.

2. **Run the Script**:

   ```bash
   python dm.py
   ```

3. **Main Menu Options**:

   - `1. Start Selenium (manual login and save cookies)`
   - `2. Start Auto DM Twitter`
   - `3. Exit`
noted : if you login twitter account for the first time, bot will reset to save your cookies data. rerun the bot to test account data in cookies and run auto dm.

4. Follow the on-screen instructions to complete the setup and start sending DMs.

## File Structure

- `data.txt`: List of Twitter usernames.
- `message.txt`: Custom message to send.
- `dm_log.csv`: Log file for DM results.
- `cookies/`: Directory to store session cookies.

## Customization

- The script features a custom purple and pink theme.
- A personalized watermark with the text "1ns1de" is displayed on the main menu.

## Notes

- Ensure your Twitter account complies with Twitter's policies to avoid account restrictions.
- Use this script responsibly.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Disclaimer

This script is for educational purposes only. The author is not responsible for any misuse or consequences resulting from the use of this script.

---

**Developed by [1ns1de]**

