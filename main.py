import yfinance as yf
import matplotlib.pyplot as plt
import openai
from datetime import datetime, timedelta

# Set your OpenAI API key
openai.api_key = "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"  # Replace with your actual key

def fetch_data(ticker_symbol, period="1mo", interval="1d"):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period, interval=interval)
    return data

def plot_data(data, ticker_symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['Close'], label='Close Price')
    plt.title(f"{ticker_symbol} Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    filename = f"{ticker_symbol}_trend.png"
    plt.savefig(filename)
    plt.close()
    return filename

def generate_summary(ticker_symbol, data):
    recent_close = data['Close'].iloc[-1]
    old_close = data['Close'].iloc[0]
    change = recent_close - old_close
    percent_change = (change / old_close) * 100

    trend = "increased 📈" if change > 0 else "decreased 📉"
    direction = "bullish" if change > 0 else "bearish"

    prompt = (
        f"The stock/crypto {ticker_symbol} has {trend} from ${old_close:.2f} "
        f"to ${recent_close:.2f} over the last month ({percent_change:.2f}%). "
        f"Summarize this in plain English and give investment insight for a casual investor."
    )

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message.content

def main():
    ticker = input("Enter a stock or crypto symbol (e.g., AAPL, BTC-USD): ").upper()
    data = fetch_data(ticker)

    if data.empty:
        print("No data found. Please check the symbol.")
        return

    image_path = plot_data(data, ticker)
    print(f"Trend image saved as: {image_path}")

    summary = generate_summary(ticker, data)
    print("\n🔍 Summary Report:\n")
    print(summary)

if __name__ == "__main__":
    main()
