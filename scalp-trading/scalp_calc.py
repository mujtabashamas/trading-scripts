# scalp_calc.py
# Optimized for Binance spot trading profit calculator
import os, sys

# Binance spot trading fee rates
BINANCE_NORMAL_FEE = 0.0010  # 0.10% per trade (0.20% total for buy+sell)
BINANCE_BNB_FEE = 0.00075   # 0.075% per trade (0.15% total for buy+sell) with BNB discount

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

def calc_profit(entry, exit, position_size, use_bnb_discount=False, leverage=1):
    """
    Calculate profit/loss for a trade
    """
    # Determine fee rate based on BNB discount
    fee_rate = BINANCE_BNB_FEE if use_bnb_discount else BINANCE_NORMAL_FEE
    
    price_change_pct = (exit - entry) / entry
    gross_pct = price_change_pct * leverage
    gross_profit = position_size * gross_pct
    total_fees = position_size * fee_rate
    net_profit = gross_profit - total_fees
    
    return {
        "price_change": round(price_change_pct * 100, 3),
        "gross_amount": round(gross_profit, 2),
        "fees": round(total_fees, 2),
        "net_amount": round(net_profit, 2)
    }


def format_currency(value):
    """Format value as currency with dollar sign"""
    return f"${value:,.2f}"

def print_scenario(title, result):
    """Print a concise scenario result with colors"""
    if result['net_amount'] >= 0:
        colorized_title = colorize_positive(title)
        colorized_values = colorize_positive(f"{result['price_change']:.2f}% | Net: {format_currency(result['net_amount'])}")
    else:
        colorized_title = colorize_negative(title)
        colorized_values = colorize_negative(f"{result['price_change']:.2f}% | Net: {format_currency(result['net_amount'])}")

    print(f"{colorized_title:<12}: {colorized_values}")

if __name__ == "__main__":
    # Get all parameters from command line arguments
    if len(sys.argv) < 5:
        print("Usage: python scalp_calc.py <entry_price> <take_profit> <stop_loss> <position_size> [--bnb]")
        print("  entry_price: your entry price")
        print("  take_profit: take profit exit price")
        print("  stop_loss: stop loss exit price")
        print("  position_size: USD size of position")
        print("  --bnb: use BNB discount fee rate (optional)")
        sys.exit(1)
    
    entry = float(sys.argv[1])
    take_profit = float(sys.argv[2])
    stop_loss = float(sys.argv[3])
    position_size = float(sys.argv[4])
    use_bnb = "--bnb" in sys.argv
    
    # Calculate profit scenario
    profit_result = calc_profit(entry, take_profit, position_size, use_bnb_discount=use_bnb, leverage=1)

    # Calculate loss scenario
    loss_result = calc_profit(entry, stop_loss, position_size, use_bnb_discount=use_bnb, leverage=1)

    print_scenario("TAKE PROFIT", profit_result)
    print_scenario("STOP LOSS", loss_result)
