import json

stocks_list = ['bitcoin','cardano','dogecoin','ethereum','solana','tether','tron']
stocks = "%2C".join(stocks_list)

URL = f"https://api.coingecko.com/api/v3/simple/price?ids={stocks}&vs_currencies=INR&include_market_cap=true&include_24hr_vol=true&include_24hr_change=false&include_last_updated_at=false"
