#!/usr/bin/env python3
# trading_strategy.py
# Advanced trading strategy calculator with AI suggestions

import os, sys
import requests
import json
from dotenv import load_dotenv
from scalp_calc import calc_profit, format_currency

# Load environment variables
load_dotenv()

# ANSI color codes for output
RESET = "\033[0m"
BOLD = "\033[1m"

# 24-bit RGB (truecolor) escape builder
def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

TRUE_GREEN = rgb(0, 255, 0)
TRUE_RED = rgb(255, 0, 0)
TRUE_BLUE = rgb(0, 150, 255)
TRUE_YELLOW = rgb(255, 255, 0)

def supports_truecolor():
    return os.environ.get("COLORTERM", "").lower() == "truecolor"

def colorize_positive(s):
    if supports_truecolor():
        return f"{BOLD}{TRUE_GREEN}{s}{RESET}"
    return f"{BOLD}\033[92m{s}{RESET}"

def colorize_negative(s):
    if supports_truecolor():
        return f"{BOLD}{TRUE_RED}{s}{RESET}"
    return f"{BOLD}\033[91m{s}{RESET}"

def colorize_info(s):
    if supports_truecolor():
        return f"{BOLD}{TRUE_BLUE}{s}{RESET}"
    return f"{BOLD}\033[94m{s}{RESET}"

def colorize_warning(s):
    if supports_truecolor():
        return f"{BOLD}{TRUE_YELLOW}{s}{RESET}"
    return f"{BOLD}\033[93m{s}{RESET}"

# OpenAI API integration
def get_ai_suggestion(token, entry_price, take_profit, stop_loss, position_size, current_price=None):
    """Get AI-powered trading strategy suggestions with technical analysis"""
    api_key = os.getenv('OPENAI_KEY')
    if not api_key:
        return "⚠️  OpenAI API key not found. Set OPENAI_KEY in .env file."

    if api_key == 'your_openai_api_key_here' or api_key == 'your_actual_api_key_here':
        return "⚠️  Please replace the placeholder with your actual OpenAI API key."

    # Fetch candlestick data for multiple timeframes
    print("📊 Fetching technical data...")
    candle_1m = get_candlestick_data(token, '1m', 240)  # Last 4 hours (240 minutes)
    status_1m = f"✅ {len(candle_1m)} candles" if isinstance(candle_1m, list) else f"❌ {str(candle_1m)[:50]}..."
    print(f"   1m candles: {status_1m}")

    candle_15m = get_candlestick_data(token, '15m', 26)  # Same day (~26 periods)
    status_15m = f"✅ {len(candle_15m)} candles" if isinstance(candle_15m, list) else f"❌ {str(candle_15m)[:50]}..."
    print(f"   15m candles: {status_15m}")

    candle_1h = get_candlestick_data(token, '1h', 48)  # Last 48 hours
    status_1h = f"✅ {len(candle_1h)} candles" if isinstance(candle_1h, list) else f"❌ {str(candle_1h)[:50]}..."
    print(f"   1h candles: {status_1h}")

    candle_1w = get_candlestick_data(token, '1w', 3)   # Last 3 weeks
    status_1w = f"✅ {len(candle_1w)} candles" if isinstance(candle_1w, list) else f"❌ {str(candle_1w)[:50]}..."
    print(f"   1w candles: {status_1w}")

    candle_1M = get_candlestick_data(token, '1M', 12)  # Last 12 months
    status_1M = f"✅ {len(candle_1M)} candles" if isinstance(candle_1M, list) else f"❌ {str(candle_1M)[:50]}..."
    print(f"   1M candles: {status_1M}")

    print("\n🤖 Analyzing with AI...")

    # Analyze each timeframe
    analysis_1m = analyze_candles(candle_1m, '1m')
    analysis_15m = analyze_candles(candle_15m, '15m')
    analysis_1h = analyze_candles(candle_1h, '1h')
    analysis_1w = analyze_candles(candle_1w, '1w')
    analysis_1M = analyze_candles(candle_1M, '1M')

    # Calculate risk metrics
    risk_amount = abs(entry_price - stop_loss) / entry_price * 100
    reward_amount = abs(take_profit - entry_price) / entry_price * 100
    risk_reward_ratio = reward_amount / risk_amount if risk_amount > 0 else 0

    profit_result = calc_profit(entry_price, take_profit, position_size)
    loss_result = calc_profit(entry_price, stop_loss, position_size)

    # Build technical analysis string
    tech_analysis = ""
    for analysis in [analysis_1m, analysis_15m, analysis_1h, analysis_1w, analysis_1M]:
        if isinstance(analysis, dict):
            tech_analysis += f"""
{analysis['timeframe']} Analysis:
- Trend: {analysis['trend']}
- Volatility: {analysis['volatility_pct']:.2f}%
- 10-period High: ${analysis['high_10']:.4f}
- 10-period Low: ${analysis['low_10']:.4f}
- Recent closes: {[f'{c:.4f}' for c in analysis['recent_closes']]}
"""
        else:
            tech_analysis += f"{analysis}\n"

    prompt = f"""
    Analyze this trading scenario with technical data and provide strategic advice:

    TOKEN: {token}
    CURRENT PRICE: ${current_price:.4f}

    PROPOSED TRADE:
    - Entry Price: ${entry_price:.4f}
    - Take Profit: ${take_profit:.4f}
    - Stop Loss: ${stop_loss:.4f}
    - Position Size: ${position_size}
    - Risk/Reward Ratio: {risk_reward_ratio:.2f}

    FINANCIAL IMPACT:
    - Potential Profit: ${profit_result['net_amount']} ({profit_result['price_change']:.2f}%)
    - Potential Loss: ${loss_result['net_amount']} ({loss_result['price_change']:.2f}%)

    TECHNICAL ANALYSIS:
    {tech_analysis}

    Based on the technical analysis across multiple timeframes, provide ONLY a JSON response with this exact structure. Do not include any explanations, markdown formatting, or additional text:

    {{
      "risk_assessment": {{
        "level": "Low|Medium|High",
        "reasoning": "Brief explanation of risk factors"
      }},
      "direction": "Long|Short",
      "strategic_recommendation": "Enter|Hold|Wait|Exit",
      "suggested_levels": {{
        "take_profit": 186.50,
        "stop_loss": 181.50
      }},
      "technical_considerations": "Key insights from candlestick patterns and trends",
      "position_size_adjustment": "Recommended position size or percentage change",
      "confidence_score": 75
    }}

    Return ONLY the JSON object. Use specific price levels from the technical data. Direction should be "Long" for buying/expecting price increase, "Short" for selling/expecting price decrease. Confidence score should be 0-100 based on signal strength.
    """

    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4o-mini',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_completion_tokens': 400,
                'temperature': 0.7
            },
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            try:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Unknown error')
                return f"❌ OpenAI API Error ({response.status_code}): {error_message}"
            except:
                return f"❌ API Error: {response.status_code} - {response.text[:200]}"

    except Exception as e:
        return f"❌ Connection Error: {str(e)}"

# Binance API endpoints
BINANCE_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"
BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"

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

def get_candlestick_data(symbol, interval, limit=50):
    """Fetch candlestick data from Binance API"""
    try:
        params = {
            'symbol': f'{symbol}USDT',
            'interval': interval,
            'limit': limit
        }
        response = requests.get(BINANCE_KLINES_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Parse candlestick data
        candles = []
        for candle in data:
            candles.append({
                'timestamp': int(candle[0]),
                'open': float(candle[1]),
                'high': float(candle[2]),
                'low': float(candle[3]),
                'close': float(candle[4]),
                'volume': float(candle[5])
            })

        return candles
    except requests.exceptions.RequestException as e:
        return f"Error fetching candlestick data: {e}"
    except (KeyError, ValueError) as e:
        return f"Error parsing candlestick data: {e}"

def analyze_candles(candles, timeframe):
    """Analyze candlestick data for key levels and trends"""
    if isinstance(candles, str):  # Error message
        return candles

    if len(candles) < 5:
        return f"Insufficient {timeframe} data"

    recent_candles = candles[-10:]  # Last 10 candles for analysis

    # Calculate key metrics
    closes = [c['close'] for c in recent_candles]
    highs = [c['high'] for c in recent_candles]
    lows = [c['low'] for c in recent_candles]

    current_price = closes[-1]
    high_10 = max(highs)
    low_10 = min(lows)
    avg_volume = sum([c['volume'] for c in recent_candles]) / len(recent_candles)

    # Trend analysis
    if closes[-1] > closes[0]:
        trend = "upward"
    elif closes[-1] < closes[0]:
        trend = "downward"
    else:
        trend = "sideways"

    # Volatility
    volatility = ((high_10 - low_10) / current_price) * 100

    return {
        'timeframe': timeframe,
        'current_price': current_price,
        'high_10': high_10,
        'low_10': low_10,
        'trend': trend,
        'volatility_pct': volatility,
        'avg_volume': avg_volume,
        'recent_closes': closes[-5:]  # Last 5 closes for pattern analysis
    }

def print_scenario(title, result):
    """Print a concise scenario result with colors"""
    if result['net_amount'] >= 0:
        colorized_title = colorize_positive(title)
        colorized_values = colorize_positive(f"{result['price_change']:.2f}% | Net: {format_currency(result['net_amount'])}")
    else:
        colorized_title = colorize_negative(title)
        colorized_values = colorize_negative(f"{result['price_change']:.2f}% | Net: {format_currency(result['net_amount'])}")

    print(f"{colorized_title:<12}: {colorized_values}")

def format_ai_response(ai_response):
    """Parse and format AI JSON response nicely"""
    try:
        # Clean the response by removing markdown code blocks
        cleaned_response = ai_response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()

        data = json.loads(cleaned_response)

        # Risk assessment with color
        risk_level = data['risk_assessment']['level']
        if risk_level == 'Low':
            risk_color = colorize_positive
        elif risk_level == 'Medium':
            risk_color = colorize_warning
        else:  # High
            risk_color = colorize_negative

        print(f"🎯 {colorize_info('Strategic Analysis')}")
        print("=" * 50)

        # Risk Assessment
        print(f"⚠️  Risk Assessment: {risk_color(risk_level)}")
        print(f"   {data['risk_assessment']['reasoning']}")
        print()

        # Strategic Recommendation
        rec_color = colorize_positive if data['strategic_recommendation'] in ['Enter'] else \
                   colorize_warning if data['strategic_recommendation'] in ['Hold', 'Wait'] else \
                   colorize_negative
        print(f"📈 Strategic Recommendation: {rec_color(data['strategic_recommendation'])}")

        # Direction Recommendation
        direction = data['direction']
        dir_color = colorize_positive if direction == 'Long' else colorize_negative
        print(f"📊 Direction: {dir_color(direction)}")
        print()

        # Suggested Levels
        print(f"🎯 {colorize_info('Suggested Levels')}:")
        tp_price = data['suggested_levels']['take_profit']
        sl_price = data['suggested_levels']['stop_loss']
        print(f"   Take Profit: {colorize_positive(f'${tp_price:.4f}')}")
        print(f"   Stop Loss:  {colorize_negative(f'${sl_price:.4f}')}")
        print()

        # Technical Considerations
        print(f"📊 {colorize_info('Technical Considerations')}:")
        print(f"   {data['technical_considerations']}")
        print()

        # Position Size Adjustment
        print(f"💰 {colorize_info('Position Size')}: {data['position_size_adjustment']}")
        print()

        # Confidence Score
        confidence = data['confidence_score']
        confidence_color = colorize_positive if confidence >= 70 else \
                          colorize_warning if confidence >= 50 else \
                          colorize_negative
        print(f"🎖️  Confidence Score: {confidence_color(f'{confidence}%')}")

    except json.JSONDecodeError as e:
        # Fallback to plain text display if JSON parsing fails
        print(f"📝 {colorize_info('AI Analysis')}:")
        print("-" * 40)
        print(ai_response)
    except KeyError as e:
        print(f"❌ Error parsing AI response: Missing key {e}")
        print(f"📝 Raw response: {ai_response}")

def main():
    """Main function to handle trading strategy analysis"""
    if len(sys.argv) < 5:
        print("Usage: python trading_strategy.py <token> <take_profit_price> <stop_loss_price> <position_size> [--bnb] [--live] [--manual] [--ai]")
        print("  token: cryptocurrency symbol (e.g., BTC, ETH, SOL)")
        print("  take_profit_price: take profit exit price")
        print("  stop_loss_price: stop loss exit price")
        print("  position_size: USD size of position")
        print("  --bnb: use BNB discount fee rate (optional)")
        print("  --live: explicitly use live Binance price as entry")
        print("  --manual: manually enter entry price")
        print("  --ai: enable AI-powered strategy suggestions")
        sys.exit(1)

    token = sys.argv[1].upper()
    take_profit_price = float(sys.argv[2])
    stop_loss_price = float(sys.argv[3])
    position_size = float(sys.argv[4])
    use_bnb = "--bnb" in sys.argv
    use_live_price = "--live" in sys.argv
    use_manual_entry = "--manual" in sys.argv
    use_ai = "--ai" in sys.argv

    # Get entry price
    if use_live_price:
        entry_price = get_current_price(token)
        print(f"{colorize_info(token + 'USDT-CURR')}: ${entry_price:.4f}")
    elif use_manual_entry:
        print("Enter entry price: ", end="")
        entry_price = float(input())
    else:
        # Default to live price if neither --live nor --manual specified
        entry_price = get_current_price(token)
        print(f"{colorize_info(token + 'USDT-CURR')}: ${entry_price:.4f}")

    # Calculate scenarios
    profit_result = calc_profit(entry_price, take_profit_price, position_size, use_bnb_discount=use_bnb)
    loss_result = calc_profit(entry_price, stop_loss_price, position_size, use_bnb_discount=use_bnb)

    print()
    print_scenario("TAKE PROFIT", profit_result)
    print_scenario("STOP LOSS", loss_result)

    # Risk metrics
    risk_pct = abs(stop_loss_price - entry_price) / entry_price * 100
    reward_pct = abs(take_profit_price - entry_price) / entry_price * 100
    rr_ratio = reward_pct / risk_pct if risk_pct > 0 else 0

    print()
    print(f"{colorize_info('Risk/Reward')}: {rr_ratio:.2f} | Risk: {risk_pct:.2f}% | Reward: {reward_pct:.2f}%")

    # AI Strategy suggestion (only if --ai flag is used)
    if use_ai:
        print()

        suggestion = get_ai_suggestion(token, entry_price, take_profit_price, stop_loss_price, position_size, entry_price)
        format_ai_response(suggestion)

if __name__ == "__main__":
    main()
