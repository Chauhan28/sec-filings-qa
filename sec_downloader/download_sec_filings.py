from sec_downloader import Downloader
from sec_downloader.types import RequestedFilings
import os

save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/raw"))
os.makedirs(save_path, exist_ok=True)

downloader = Downloader("genai-sec10k-insights", "digvijayemail@gmail.com")

tickers = ["AAPL", "MSFT", "TSLA", "AMZN", "JPM", "NVDA", "WMT", "META", "KO", "PFE"]

for ticker in tickers:
    query = RequestedFilings(ticker_or_cik=ticker, form_type="10-K", limit=1)
    filings = downloader.get_filing_metadatas(query)
    if not filings:
        print(f"❌ No 10-K found for {ticker}")
        continue

    doc_url = filings[0].primary_doc_url
    content = downloader.download_filing(url=doc_url)  # ✅ Fixed line

    with open(os.path.join(save_path, f"{ticker}_10k.txt"), "wb") as f:
        f.write(content)

    print(f"✅ Downloaded {ticker} 10-K to {save_path}/{ticker}_10k.txt")
