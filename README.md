# Trading Scripts

A collection of advanced cryptocurrency trading analysis tools with real-time Binance data integration and AI-powered strategy suggestions.

## 🚀 Scripts Overview

### 1. `trading_strategy.py` - AI-Powered Strategy Analyzer
**Advanced trading analysis with AI insights and technical indicators**

**Features:**
- 🤖 **AI Strategy Analysis** - GPT-4o-mini-powered trading recommendations with structured JSON responses
- 📊 **Multi-Timeframe Analysis** - 1m (4h), 15m (1d), 1h (48h), 1w (3w), and 1M (12M) candlestick data
- 🎯 **Smart TP/SL Suggestions** - AI recommends optimal take profit and stop loss levels based on technical analysis
- 📈 **Risk/Reward Metrics** - Comprehensive risk assessment
- 🎨 **Beautiful Color Output** - Bold, color-coded results

**Usage:**
```bash
# Basic analysis with live price
python3 scalp-trading/trading_strategy.py SOL 185 182 1000

# With AI analysis
python3 scalp-trading/trading_strategy.py SOL 185 182 1000 --ai

# Manual entry price
python3 scalp-trading/trading_strategy.py SOL 185 182 1000 --manual

# Live price with AI
python3 scalp-trading/trading_strategy.py SOL 185 182 1000 --live --ai

# With BNB fee discount
python3 scalp-trading/trading_strategy.py SOL 185 182 1000 --bnb --ai
```

**Sample Output:**
```
SOLUSDT-CURR: $185.67

TAKE PROFIT: -0.36% | Net: $-4.61
STOP LOSS: -1.98% | Net: $-20.77

Risk/Reward: 0.18 | Risk: 1.98% | Reward: 0.36%

📊 Fetching technical data...
   1m candles: ✅ 240 candles (4h)
   15m candles: ✅ 26 candles (1d)
   1h candles: ✅ 48 candles (48h)
   1w candles: ✅ 3 candles (3w)
   1M candles: ✅ 12 candles (12M)
🤖 Analyzing with AI...

🎯 Strategic Analysis
==================================================
⚠️  Risk Assessment: High
   Current downward trend across multiple timeframes suggests increased likelihood of price decline.

📈 Strategic Recommendation: Exit
📊 Direction: Short

🎯 Suggested Levels:
   Take Profit: $181.5000
   Stop Loss:  $186.5000

📊 Technical Considerations:
   Recent downward trend in 1m and 1h analysis indicates bearish sentiment, while upward trend in 15m may not be strong enough to reverse the overall trend.

💰 Position Size: Reduce position size by 50%

🎖️  Confidence Score: 65%
```

### 2. `binance_price_calc.py` - Quick Profit Calculator
**Fast profit/loss calculations for spot trading**

**Features:**
- 💰 **Real-time P&L** - Live Binance price integration
- 📊 **Clean Output** - Concise, color-coded results
- 🔄 **Flexible Entry** - Live, manual, or default pricing

**Usage:**
```bash
# Live price calculation
python3 scalp-trading/binance_price_calc.py BTC 65000 62000 1000

# Manual entry price
python3 scalp-trading/binance_price_calc.py BTC 65000 62000 1000 --manual

# With BNB discount
python3 scalp-trading/binance_price_calc.py BTC 65000 62000 1000 --bnb
```

### 3. `scalp_calc.py` - Basic Calculator
**Simple profit/loss calculator without live data**

**Usage:**
```bash
python3 scalp-trading/scalp_calc.py 183.50 185.00 182.00 1000
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation
```bash
# Clone or navigate to project directory
cd /path/to/trading-scripts

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### API Setup
1. **OpenAI API Key** (for AI features):
   ```bash
   # Create .env file in project root
   echo "OPENAI_KEY=your_openai_api_key_here" > .env

   # Or edit manually:
   nano .env
   ```
   Get your API key from: https://platform.openai.com/api-keys

2. **Binance API** (no key required for basic price data)

## 📊 Features Comparison

| Feature | trading_strategy.py | binance_price_calc.py | scalp_calc.py |
|---------|-------------------|---------------------|---------------|
| Live Binance Data | ✅ | ✅ | ❌ |
| AI Analysis | ✅ | ❌ | ❌ |
| Technical Analysis | ✅ | ❌ | ❌ |
| Multi-Timeframe | ✅ | ❌ | ❌ |
| Color Output | ✅ | ✅ | ❌ |
| Fee Calculations | ✅ | ✅ | ✅ |
| Risk/Reward | ✅ | ❌ | ❌ |

## 🎨 Color Coding

- 🟢 **Green**: Profitable scenarios, positive returns
- 🔴 **Red**: Loss scenarios, negative returns
- 🟡 **Yellow**: Warnings, AI analysis headers
- 🔵 **Blue**: Information, current prices

## 💡 Usage Tips

### For Quick Analysis
Use `binance_price_calc.py` for fast P&L calculations with live prices.

### For Strategic Planning
Use `trading_strategy.py --ai` for comprehensive analysis with AI recommendations.

### For Backtesting
Use `scalp_calc.py` with historical prices for strategy testing.

### Risk Management
- Always use stop losses
- Aim for risk/reward ratios > 1:2
- Consider position sizing based on account risk tolerance
- Use AI suggestions as guidance, not absolute rules

## 🔧 Configuration

### Environment Variables
```
OPENAI_KEY=your_openai_api_key_here
```

### Fee Settings
- **Normal**: 0.10% per trade (0.20% round trip)
- **BNB Discount**: 0.075% per trade (0.15% round trip)

## 📈 Supported Assets

All Binance spot trading pairs ending with USDT:
- BTC, ETH, SOL, ADA, DOT, etc.

## ⚠️ Disclaimer

This tool is for educational and informational purposes only. Always do your own research and never risk more than you can afford to lose. Past performance does not guarantee future results.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the trading scripts.

---

**Happy Trading!** 📊💹
