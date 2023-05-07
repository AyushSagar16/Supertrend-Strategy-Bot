# Supertrend Strategy Stock Trading Bot

This project is a Python-based stock trading bot that uses the Supertrend strategy. It uses the Alpaca Paper Trading API and Yahoo Finance API (yfinance) to gather data and make trades.

## Features

- Uses the supertrend strategy to determine when to buy and sell stocks.
- Runs only during market hours to ensure accurate and up-to-date information.
- Implements stop loss orders to minimize losses in case of unfavorable market conditions.
- Prints out all relevant data to keep users informed of the bot's activity.

## Installation

To install the required packages, use pip: `pip install alpaca-trade-api yfinance`

## Usage

Before using the bot, you need to set up an Alpaca Paper Trading account and get your API keys. You can find more information on how to do that at [https://alpaca.markets/learn/start-paper-trading/](https://alpaca.markets/learn/start-paper-trading/).

Once you have your API keys, open the `bot.py` file and replace `API_KEY` and `SECRET_KEY` with your actual keys.

To run the bot, simply run the `bot.py` script. You can customize the `stockN` and `alpacaName` variables to the stock you wish to trade.

## Running on PythonAnywhere

Since this bot dowloads live market data on a certain timeframe it is highly suggested to run it on a cloud platform such as PythonAnywhere.

To run the bot on [PythonAnywhere](https://www.pythonanywhere.com), follow these steps:

1. Create a PythonAnywhere account and log in.
2. In the dashboard, go to the "Files" tab and click "New file".
3. Name the file `bot.py` and copy the contents of `bot.py` into it.
4. Save the file and return to the dashboard.
5. Open a new console and navigate to the directory where `bot.py` is located.
6. Run the command `python bot.py` to start the bot.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

## Disclaimer

This bot is provided for educational and informational purposes only. It is not intended to be used as a financial or investment advice. The author of this bot is not liable for any losses that may arise from its use. The user assumes all responsibility and risk associated with the use of this bot.
