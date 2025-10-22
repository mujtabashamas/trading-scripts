# scalp_calc.py
# Optimized for Binance spot trading profit calculator
import sys

# Binance spot trading fee rates
BINANCE_NORMAL_FEE = 0.0010  # 0.10% per trade (0.20% total for buy+sell)
BINANCE_BNB_FEE = 0.00075   # 0.075% per trade (0.15% total for buy+sell) with BNB discount

def calc_profit(entry, exit, position_size, use_bnb_discount=False, leverage=1):
    """
    entry: entry price (float)
    exit: exit price (float)
    position_size: USD size of position
    use_bnb_discount: whether to use BNB discount fee rate
    leverage: leverage multiplier (1x for spot trading)
    """
    # Determine fee rate based on BNB discount
    fee_rate = BINANCE_BNB_FEE if use_bnb_discount else BINANCE_NORMAL_FEE
    
    price_change_pct = (exit - entry) / entry
    gross_pct = price_change_pct * leverage
    gross_profit = position_size * gross_pct
    total_fees = position_size * fee_rate
    net_profit = gross_profit - total_fees
    
    return {
        "price_change_%": round(price_change_pct * 100, 3),
        "gross_%": round(gross_pct * 100, 3),
        "gross_profit": round(gross_profit, 2),
        "fees": round(total_fees, 2),
        "net_profit": round(net_profit, 2),
        "fee_rate_used": "BNB discount" if use_bnb_discount else "Normal"
    }


if __name__ == "__main__":
    # Get position size from command line argument
    if len(sys.argv) < 2:
        print("Usage: python scalp_calc.py <position_size> [--bnb]")
        print("  position_size: USD size of position")
        print("  --bnb: use BNB discount fee rate (optional)")
        sys.exit(1)
    
    position_size = float(sys.argv[1])
    use_bnb = "--bnb" in sys.argv
    
    # Only ask for entry and exit prices
    entry = float(input("Entry price: "))
    exit = float(input("Exit price: "))
    
    result = calc_profit(entry, exit, position_size, use_bnb_discount=use_bnb, leverage=1)
    
    print(f"\n📊 Results (Position: ${position_size})")
    print(f"Fee rate: {result['fee_rate_used']}")
    for k, v in result.items():
        if k != "fee_rate_used":
            print(f"{k:15}: {v}")
