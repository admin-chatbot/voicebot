import finnhub
finnhub_client = finnhub.Client(api_key="cll916pr01qhqdq2qjqgcll916pr01qhqdq2qjr0")

print(finnhub_client.symbol_lookup('apple'))