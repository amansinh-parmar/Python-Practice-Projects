# Input from User
pair = input('Enter your Forex Pair (XAUUSD/EURUSD/JPYUSD): ').upper()
trade_type = input('BUY or SELL: ').upper()

entry = float(input('Enter Entry Price: '))
exit_price = float(input('Enter Exit Price: '))
lot = float(input('Enter Lot Size: '))

# Calculate Pair
customize_pair = {
    'XAUUSD': 100,
    'EURUSD': 100000,
    'JPYUSD': 100000,
}
customize_pairs = customize_pair[pair]

if pair not in customize_pair:
    print('Invalid Pair')
    exit_price()

# Calculate Pips
pips = {
    'XAUUSD': 0.01,
    'EURUSD': 0.0001,
    'JPYUSD': 0.01,
}

pip_size = pips[pair]

if trade_type not in ['BUY', "SELL"]:
    print('Invalid Trade Type!!')
    exit_price()

# Calculate the PIP Size
if trade_type == 'BUY':
    pip = (exit_price - entry) / pip_size
else: 
    pip = (entry - exit_price) / pip_size

# Calculate the P/L 
if trade_type == 'BUY':
    result = (exit_price - entry) * customize_pairs * lot
else:
    result = (entry - exit_price) * customize_pairs * lot

print(' ------- Trade Summary ------- ')
print(f'Forex Pair: {pair}')
print(f'Trade Type: {trade_type}\n')

print(f'Entry Price: {entry}')
print(f'Exit Prince: {exit_price}')
print(f'Lot Size: {lot}\n')

print(f'Total Pips: {round(pip)}')
print('=================================')
print(f'Tota Profit/Loss: ${round(result)}\n')

if result > 0:
    print('- Congratulation, You are in PROFIT.')
elif result < 0:
    print('Today is your LOSS DAY, Apply KILL SWITCH.')
else:
    print('Today You are in BREAK-EVEN.')