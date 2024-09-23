# Koi Bot

Welcome to **Koi**, an open-source Discord bot built with Python, designed to enhance your experience in **Honkai: Star Rail** while providing a variety of utility and moderation commands. Koi integrates with multiple APIs, including the Honkai: Star Rail API and the Retroachievements API, to fetch relevant game data for users.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Honkai: Star Rail Integration**: Retrieve character stats, weapon information, and more.
- **Retroachievements Integration**: Access achievements for retro games.
- **Utility Commands**: Fun commands like polls and reminders.
- **Moderation Tools**: Commands to manage your server effectively.

## Installation

To set up Koi on your local machine, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/koi-bot.git
   cd koi-bot
   ```

2. **Set up a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   Ensure you have [Python 3.11.5](https://www.python.org/downloads/release/python-3115/) installed. I say this as this is the version I used to run the bot. 
   Then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables**:
   The bot token should be placed in a file at the root of the repository named `token.txt`
   Your api information for Retroachievements API should go in a file called `api_info.txt`

6. **Start the bot**:
   ```bash
   python main.py
   ```

## Configuration

You can customize whatever you like about this bot as it is fully open source.
Note: To successfully run some commands, you may have to replace every instance of my discord user id with yours.

## Usage

Once Koi is up and running, invite it to your Discord server and start using the available commands. Ensure the bot has the necessary permissions to function properly.
You will also have to sync the bot's command tree

## Commands

Here’s a brief overview of some commands you can use with Koi:


### Honkai: Star Rail Commands

- **/hsr [UID]**: Get information about a Honkai: Star Rail player from their UID

### Retroachievements Commands

- **/retro-profile [username]**: Fetches user information from their username on retroachievements.

### Utility Commands

- **/restart**: Restarts the bot, owner only.
- **/base64-encode**: Converts the given text to base64.
- **/base64-decode**: Converts the given base64 text to utf-8.
- **/avatar [?user]**: Retrieves a user's avatar, if none is provided, displays your own avatar.
- **/invite**: Sends an embed with an invite link to the discord bot.
- **/sync**: Syncs the bot's command tree.

### Entertainment Commands

- **/hug [user]**: Sends a hug gif and pings the mentioned user.
- **/flip**: Flips a coin.
- **/ping**: Pong!

## Contributing

We welcome contributions to Koi! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

Please ensure that your code adheres to the existing style and includes appropriate tests where applicable.

## License

Koi is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or issues, feel free to open an issue on the GitHub repository or reach out via Discord:

- Discord: `@lluunnaa.` Including the period.

Thank you for using Koi! We hope you enjoy its features and capabilities.
