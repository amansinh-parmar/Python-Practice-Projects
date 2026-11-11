print("------- Trading Calculator ------- ")

# Forex & Gold Trading P/L Calculator
pair = input("Enter your Forex Pair (XAUUSD/EURUSD/JPYUSD): ").upper()
trade_type = input("BUY or SELL: ").upper()

entry = float(input("Enter Entry Price: "))
exit_price = float(input("Enter Exit Price: "))
lot_size = float(input("Enter Lot Size: "))

# Contract Sizes
contract_size = {
    "XAUUSD": 100,
    "EURUSD": 100000,
    "JPYUSD": 100000,
}
customize_pairs = contract_size[pair]

# Check pair
if pair not in contract_size:
    print("Invalid Pair")
    exit_price()

# Pip sizes
pips = {
    "XAUUSD": 0.01,
    "EURUSD": 0.0001,
    "JPYUSD": 0.01,
}
pip_size = pips[pair]

# Check pair
if pair not in contract_size:
    print("Invalid Pair!!")
    exit_price()

# Check trade type
if trade_type not in ["BUY", "SELL"]:
    print("Invalid Trade Type!!")
    exit_price()

# Calculate Pip Size
if trade_type == "BUY":
    pips = (exit_price - entry) / pip_size
else:
    pips = (entry - exit_price) / pip_size

# Calculate P/L in quote currency
if trade_type == "BUY":
    profit_loss = (exit_price - entry) * customize_pairs * lot_size
else:
    profit_loss = (entry - exit_price) * customize_pairs * lot_size


# Display results
print("-------- Trade Summary -------- ")
print(f"Forex Pair: {pair}")
print(f"Trade Type: {trade_type}\n")

print(f"Entry Price: {entry}")
print(f"Exit Prince: {exit_price}")
print(f"Lot Size: {lot_size}\n")

print(f"Total Pips: {round(pips, 2)}")
print("===========================")
print(f"Tota Profit/Loss: ${round(profit_loss, 2)}\n")

if profit_loss > 0:
    print("- Congratulation, You are in PROFIT.")
elif profit_loss < 0:
    print("Today is your LOSS DAY, Apply KILL SWITCH.")
else:
    print("Today You are in BREAK-EVEN.")
