# Twitter Auto DM Bot 🤖

An automated Twitter Direct Message sender built with Python and Selenium. This bot allows you to send personalized direct messages to multiple Twitter users automatically, with customizable delay times and cookie management.

## ✨ Features

- **Cookie-based Authentication**: Saves login sessions to avoid frequent logins
- **Customizable Messages**: Support for both single and multiple message templates
- **Smart Delay System**: Adjustable delay between messages to avoid spam detection
- **Progress Tracking**: Real-time progress updates with tqdm
- **Error Handling**: Comprehensive error handling and logging
- **CSV Logging**: Tracks message delivery status for each user
- **User-friendly Interface**: Clean CLI interface with colored output

## 🛠️ Requirements

- Python 3.7+
- Chrome Browser
- Required Python packages:
  ```
  selenium>=4.0.0
  chromedriver-autoinstaller>=0.4.0
  tqdm
  colorama
  ```

## 🛋️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/1ns1de1ns1de/twitter-auto-dm.git
   cd twitter-auto-dm
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 📝 Configuration

1. Create required files in the project directory:
   - `data.txt`: List of target usernames (one per line)
   - `message.txt`: Message template(s) to send
   - A `cookies` folder will be automatically created

2. Format examples:
   - `data.txt`:
     ```
     username1
     username2
     username3
     ```
   - `message.txt`:
     ```
     Hello {username},
     This is my message.
     ```

## 🚀 Usage

1. Run the script:
   ```bash
   python dm.py
   ```

2. Available options in the menu:
   - **Option 1**: Start Selenium (manual login and save cookies)
   - **Option 2**: Start Auto DM Twitter
   - **Option 3**: Update Delay Settings
   - **Option 4**: Exit

3. First-time setup:
   - Choose Option 1
   - Log in to Twitter manually when prompted
   - Wait for cookies to be saved

4. Sending messages:
   - Choose Option 2
   - The bot will automatically:
     - Load saved cookies
     - Search for each username
     - Send messages with specified delays
     - Log results to CSV

## ⚙️ Customization

### Delay Settings
- Default delay: 10-40 seconds between messages
- Can be modified through Option 3 in the menu
- Recommended to keep delays random and reasonable

### Message Format
- Supports both single and multiple messages
- If multiple messages are provided, they'll be used in rotation
- Can include basic formatting

## 📊 Logging

The bot creates `dm_log.csv` with the following information:
- Username
- Message delivery status
- Timestamp

## ⚠️ Important Notes

1. **Rate Limiting**:
   - Use reasonable delays between messages
   - Monitor Twitter's rate limits
   - Avoid sending too many messages in a short time

2. **Account Safety**:
   - Use with caution
   - Follow Twitter's terms of service
   - Avoid spam-like behavior

3. **Error Handling**:
   - The bot includes comprehensive error handling
   - Failed messages are logged
   - Interruptions can be handled gracefully

## 🔒 Security

- Cookies are stored locally in the `cookies` folder
- No passwords are stored
- Use on trusted machines only

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📚 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

- **1ns1de**
- GitHub: [@1ns1de1ns1de](https://github.com/1ns1de1ns1de)

## 🙏 Acknowledgments

- Selenium WebDriver team
- Python community
- All contributors and testers

## ⚠️ Disclaimer

This bot is for educational purposes only. Use at your own risk and responsibility. The author is not responsible for any misuse or any Twitter account restrictions that may result from using this bot.

---
Made with ❤️ by 1ns1de

