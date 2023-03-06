# ENTRY Strategy
IF close crosses supertrend or close crosses 2 consecutive green bars or a big range bar (out of last 5 bars on the underlying stock) , enter(Buy ATM CALL) at the break of bar high(all bars are one minute)
# Stop
Stop at decision bar Low and increase it to breakeven if bar has crossed the range of the decision Bar



# Exit Strategy
IF close crosses above supertrend or if there are 2 consecutive red bars or a big red range bar (out of last 5 bars on the underlying stock) , exit at the break of bar low

# Summary

Data is collected using the ibkr api for the start strategies shared above. in addition, supertrend function and option trading functions have been added to the backtrader library in order to backtest this data for the options exchange.