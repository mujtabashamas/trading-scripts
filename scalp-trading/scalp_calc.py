# scalp_calc.py
# Optimized for Binance spot trading profit calculator
import sys

# Binance spot trading fee rates
BINANCE_NORMAL_FEE = 0.0010  # 0.10% per trade (0.20% total for buy+sell)
BINANCE_BNB_FEE = 0.00075   # 0.075% per trade (0.15% total for buy+sell) with BNB discount

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
    """Print a formatted scenario table"""
    print(f"\n{title}")
    print("=" * 35)
    print("PERCENTAGES")
    print(f"Price Change: {result['price_change']:.3f}%")
    print("-" * 35)
    print("AMOUNTS")
    print(f"Gross: {format_currency(result['gross_amount'])}")
    print(f"Fees : {format_currency(result['fees'])}")
    print(f"Net  : {format_currency(result['net_amount'])}")
    print("=" * 35)

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
    
    # Determine fee rate for display
    fee_rate = "BNB discount (0.075%)" if use_bnb else "Normal (0.10%)"
    
    print(f"📊 Trade Analysis (Position: {format_currency(position_size)})")
    print(f"Entry Price       {entry:.4f}")
    print(f"Take Profit       {take_profit:.4f}")
    print(f"Stop Loss         {stop_loss:.4f}")
    print(f"Fee Rate          {fee_rate}")
    
    # Calculate profit scenario
    profit_result = calc_profit(entry, take_profit, position_size, use_bnb_discount=use_bnb, leverage=1)
    
    # Calculate loss scenario  
    loss_result = calc_profit(entry, stop_loss, position_size, use_bnb_discount=use_bnb, leverage=1)
    
    print_scenario("✅ TAKE PROFIT", profit_result)
    print_scenario("❌ STOP LOSS", loss_result)
