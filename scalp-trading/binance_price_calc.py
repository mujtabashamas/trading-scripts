#!/usr/bin/env python3
# binance_price_calc.py
# Fetch current price from Binance and calculate profit

import sys
import requests
from scalp_calc import calc_profit, format_currency

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

def print_current_result(result):
    """Print current price result in clean format"""
    print("=" * 35)
    print("PERCENTAGES")
    print(f"Price Change: {result['price_change']:.3f}%")
    print("-" * 35)
    print("AMOUNTS")
    print(f"Gross: {format_currency(result['gross_amount'])}")
    print(f"Fees : {format_currency(result['fees'])}")
    print(f"Net  : {format_currency(result['net_amount'])}")
    print("=" * 35)

def main():
    """Main function to handle command line arguments and calculations"""
    if len(sys.argv) < 4:
        print("Usage: python binance_price_calc.py <token> <entry_price> <position_size> [--bnb]")
        print("  token: cryptocurrency symbol (e.g., BTC, ETH, SOL)")
        print("  entry_price: your entry price")
        print("  position_size: USD size of position")
        print("  --bnb: use BNB discount fee rate (optional)")
        sys.exit(1)
    
    token = sys.argv[1].upper()
    entry_price = float(sys.argv[2])
    position_size = float(sys.argv[3])
    use_bnb = "--bnb" in sys.argv
    
    # Get current price from Binance
    current_price = get_current_price(token)
    
    print(f"🔍 Fetching current price for {token}USDT...")
    print(f"Current price: ${current_price:.4f}")
    print(f"Your entry price: ${entry_price:.4f}")
    
    # Calculate profit using existing function
    result = calc_profit(entry_price, current_price, position_size, use_bnb_discount=use_bnb, leverage=1)

    # Determine fee rate for display
    fee_rate = "BNB discount (0.075%)" if use_bnb else "Normal (0.10%)"

    print(f"\n📊 Current Price Analysis (Position: {format_currency(position_size)})")
    print(f"Entry Price     : ${entry_price:.4f}")
    print(f"Current Price   : ${current_price:.4f}")
    print(f"Fee Rate        : {fee_rate}")

    print_current_result(result)

if __name__ == "__main__":
    main()
