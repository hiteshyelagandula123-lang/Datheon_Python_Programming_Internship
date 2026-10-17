
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STOCKS_FILE = BASE_DIR / "stocks.csv"
SUMMARY_FILE = BASE_DIR / "portfolio_summary.csv"

# Sample prices for testing. These are not live market prices.
SAMPLE_PRICES = {
    "MMM": 145.00,
    "AOS": 72.50,
    "ABT": 118.00,
    "ABBV": 195.00,
    "ACN": 245.00,
    "ADBE": 350.00,
    "AMD": 165.00,
    "AMZN": 220.00,
    "AAPL": 250.00,
    "MSFT": 510.00,
}


def load_symbols():
    """Load valid ticker symbols from the provided company dataset."""
    symbols = set()

    if not STOCKS_FILE.exists():
        print(f"Warning: {STOCKS_FILE.name} not found.")
        return symbols

    with STOCKS_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            symbol = row.get("Symbol", "").strip().upper()
            if symbol:
                symbols.add(symbol)

    return symbols


def get_positive_number(prompt, allow_zero=False):
    """Read a valid positive number from the user."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0 or (value == 0 and not allow_zero):
                print("Enter a valid positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def save_summary(holdings):
    """Write holdings and portfolio totals to a CSV file."""
    with SUMMARY_FILE.open("w", newline="", encoding="utf-8") as file:
        fields = [
            "Symbol",
            "Shares",
            "Purchase Price",
            "Current Price",
            "Invested Amount",
            "Current Value",
            "Gain/Loss",
            "Gain/Loss (%)",
        ]

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for item in holdings:
            writer.writerow({
                "Symbol": item["symbol"],
                "Shares": item["shares"],
                "Purchase Price": f'{item["purchase_price"]:.2f}',
                "Current Price": f'{item["current_price"]:.2f}',
                "Invested Amount": f'{item["invested"]:.2f}',
                "Current Value": f'{item["current_value"]:.2f}',
                "Gain/Loss": f'{item["gain_loss"]:.2f}',
                "Gain/Loss (%)": f'{item["gain_loss_pct"]:.2f}',
            })

        total_invested = sum(item["invested"] for item in holdings)
        total_value = sum(item["current_value"] for item in holdings)

        writer.writerow({
            "Symbol": "TOTAL",
            "Shares": "",
            "Purchase Price": "",
            "Current Price": "",
            "Invested Amount": f"{total_invested:.2f}",
            "Current Value": f"{total_value:.2f}",
            "Gain/Loss": f"{total_value - total_invested:.2f}",
            "Gain/Loss (%)": (
                f"{(total_value - total_invested) / total_invested * 100:.2f}"
                if total_invested else "0.00"
            ),
        })


def main():
    valid_symbols = load_symbols()
    holdings = []

    print("\n=== STOCK PORTFOLIO PERFORMANCE TRACKER ===")
    print("Price source: illustrative sample prices, NOT live market data.")

    if not valid_symbols:
        print("No company symbols loaded. Check that stocks.csv exists.")
        return

    print(f"Loaded {len(valid_symbols)} company symbols from stocks.csv.")
    print("Sample-priced symbols:", ", ".join(SAMPLE_PRICES))
    print("\nEnter your holdings. Type DONE when finished.")

    while True:
        symbol = input("\nStock ticker: ").strip().upper()

        if symbol == "DONE":
            break

        if not symbol:
            print("Ticker cannot be empty.")
            continue

        if symbol not in valid_symbols:
            print("Ticker not found in stocks.csv. Please try again.")
            continue

        if symbol not in SAMPLE_PRICES:
            print("No sample price is configured for this ticker yet.")
            print("Choose a symbol from the sample-priced list.")
            continue

        shares = get_positive_number("Number of shares: ")
        purchase_price = get_positive_number("Purchase price per share: ")

        current_price = SAMPLE_PRICES[symbol]
        invested = shares * purchase_price
        current_value = shares * current_price
        gain_loss = current_value - invested
        gain_loss_pct = gain_loss / invested * 100 if invested else 0

        holdings.append({
            "symbol": symbol,
            "shares": shares,
            "purchase_price": purchase_price,
            "current_price": current_price,
            "invested": invested,
            "current_value": current_value,
            "gain_loss": gain_loss,
            "gain_loss_pct": gain_loss_pct,
        })

        print(f"Added {symbol} successfully.")

    if not holdings:
        print("No holdings entered. Nothing to save.")
        return

    print("\n=== PORTFOLIO SUMMARY ===")
    print(
        f"{'Symbol':<8}{'Shares':>10}{'Invested':>14}"
        f"{'Current Value':>17}{'Gain/Loss':>14}{'Return %':>12}"
    )
    print("-" * 75)

    for item in holdings:
        print(
            f"{item['symbol']:<8}{item['shares']:>10.2f}"
            f"{item['invested']:>14.2f}"
            f"{item['current_value']:>17.2f}"
            f"{item['gain_loss']:>14.2f}"
            f"{item['gain_loss_pct']:>12.2f}"
        )

    total_invested = sum(item["invested"] for item in holdings)
    total_value = sum(item["current_value"] for item in holdings)
    total_gain_loss = total_value - total_invested
    total_return = (
        total_gain_loss / total_invested * 100 if total_invested else 0
    )

    print("-" * 75)
    print(f"Total invested:   ${total_invested:.2f}")
    print(f"Current value:    ${total_value:.2f}")
    print(f"Total gain/loss:  ${total_gain_loss:.2f}")
    print(f"Portfolio return: {total_return:.2f}%")

    save_summary(holdings)
    print(f"\nSummary saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
