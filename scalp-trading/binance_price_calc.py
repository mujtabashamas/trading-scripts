#!/usr/bin/env python3
# binance_price_calc.py
# Fetch current price from Binance as entry price and calculate take profit/stop loss scenarios

import os, sys
import requests
from scalp_calc import calc_profit, format_currency

RESET = "\033[0m"

# 24-bit RGB (truecolor) escape builder
def rgb(r, g, b):  # foreground
    return f"\033[38;2;{r};{g};{b}m"

BOLD = "\033[1m"
TRUE_GREEN = rgb(0, 255, 0)
TRUE_RED   = rgb(255, 0, 0)  # Brighter red

def supports_truecolor():
    return os.environ.get("COLORTERM", "").lower() == "truecolor"

def colorize_positive(s):
    if supports_truecolor():
        return f"{BOLD}{TRUE_GREEN}{s}{RESET}"
    # fallback to bright ANSI
    return f"{BOLD}\033[92m{s}{RESET}"

def colorize_negative(s):
    if supports_truecolor():
        return f"{BOLD}{TRUE_RED}{s}{RESET}"
    # fallback to bright ANSI
    return f"{BOLD}\033[91m{s}{RESET}"

# Binance API endpoint for price
BINANCE_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"

def get_current_price(symbol):
    """Fetch current price from Binance API"""
    try:
        response = requests.get(f"{BINANCE_PRICE_URL}?symbol={symbol}USDT")
        response.raise_for_status()
        data = response.json()
        return float(data['price'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching price from Binance: {e}")
        sys.exit(1)
    except (KeyError, ValueError) as e:
        print(f"Error parsing response: {e}")
        sys.exit(1)

def print_scenario(title, result):
    """Print a concise scenario result with colors"""
    if result['net_amount'] >= 0:
        colorized_title = colorize_positive(title)
        colorized_values = colorize_positive(f"{result['price_change']:>6.2f}% | Net: {format_currency(result['net_amount'])}")
    else:
        colorized_title = colorize_negative(title)
        colorized_values = colorize_negative(f"{result['price_change']:>6.2f}% | Net: {format_currency(result['net_amount'])}")

    print(f"{colorized_title:<12}: {colorized_values}")

def main():
    """Main function to handle command line arguments and calculations"""
    if len(sys.argv) < 5:
        print("Usage: python binance_price_calc.py <token> <take_profit_price> <stop_loss_price> <position_size> [--bnb] [--live] [--manual]")
        print("  token: cryptocurrency symbol (e.g., BTC, ETH, SOL)")
        print("  take_profit_price: take profit exit price")
        print("  stop_loss_price: stop loss exit price")
        print("  position_size: USD size of position")
        print("  --bnb: use BNB discount fee rate (optional)")
        print("  --live: explicitly use live Binance price as entry")
        print("  --manual: manually enter entry price")
        sys.exit(1)

    token = sys.argv[1].upper()
    take_profit_price = float(sys.argv[2])
    stop_loss_price = float(sys.argv[3])
    position_size = float(sys.argv[4])
    use_bnb = "--bnb" in sys.argv
    use_live_price = "--live" in sys.argv
    use_manual_entry = "--manual" in sys.argv

    # Get entry price
    if use_live_price:
        entry_price = get_current_price(token)
        print(f"{token}USDT-CURR: ${entry_price:.4f}")
    elif use_manual_entry:
        print("Enter entry price: ", end="")
        entry_price = float(input())
    else:
        # Default to live price if neither --live nor --manual specified
        entry_price = get_current_price(token)
        print(f"{token}USDT-CURR: ${entry_price:.4f}")

    # Calculate profit scenarios
    profit_result = calc_profit(entry_price, take_profit_price, position_size, use_bnb_discount=use_bnb, leverage=1)
    loss_result = calc_profit(entry_price, stop_loss_price, position_size, use_bnb_discount=use_bnb, leverage=1)

    # Print both scenarios
    print_scenario("TAKE PROFIT", profit_result)
    print_scenario("STOP LOSS  ", loss_result)

if __name__ == "__main__":
    main()
