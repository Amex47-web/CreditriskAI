import requests
import os
import time
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Optional

class SECLoader:
    def __init__(self, download_dir: str = "data/filings", user_agent: str = "MyOpenSourceProject/1.0 (contact@example.com)"):
        """
        Initialize the SEC Loader.
        :param download_dir: Directory to save downloaded filings.
        :param user_agent: User-Agent string required by SEC EDGAR (Company Name/Email).
        """
        self.download_dir = download_dir
        self.user_agent = user_agent
        self.base_url = "https://www.sec.gov"
        self.headers = {"User-Agent": self.user_agent}
        
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def get_cik(self, ticker: str) -> Optional[str]:
        """
        Fetch CIK for a given ticker symbol using SEC company tickers JSON.
        """
        ticker = ticker.upper()
        url = "https://www.sec.gov/files/company_tickers.json"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            for key, entry in data.items():
                if entry['ticker'] == ticker:
                    return str(entry['cik_str']).zfill(10) # CIK is 10 digits
            
            print(f"CIK not found for ticker: {ticker}")
            return None
        except Exception as e:
            print(f"Error fetching CIK: {e}")
            return None

    def list_filings(self, cik: str, filing_type: str = "10-K", limit: int = 5) -> List[dict]:
        """
        List recent filings for a given CIK.
        """
        api_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        
        try:
            response = requests.get(api_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            recent = data['filings']['recent']
            filings = []
            
            for i in range(len(recent['accessionNumber'])):
                if recent['form'][i] == filing_type:
                    filings.append({
                        'accessionNumber': recent['accessionNumber'][i],
                        'filingDate': recent['filingDate'][i],
                        'reportDate': recent['reportDate'][i],
                        'form': recent['form'][i],
                        'primaryDocument': recent['primaryDocument'][i]
                    })
                    if len(filings) >= limit:
                        break
            
            return filings
        except Exception as e:
            print(f"Error listing filings: {e}")
            return []

    def download_filing(self, cik: str, accession_number: str, primary_document: str, save_name: str):
        """
        Download a specific filing document.
        """
        # Remove hyphens for the URL structure
        folder_accession = accession_number.replace("-", "")
        url = f"{self.base_url}/Archives/edgar/data/{int(cik)}/{folder_accession}/{primary_document}"
        
        try:
            print(f"Downloading {url}...")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            file_path = os.path.join(self.download_dir, save_name)
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            print(f"Saved to {file_path}")
            # Respect SEC rate limit (10 req/sec max, but be safe)
            time.sleep(0.2)
            return file_path
        except Exception as e:
            print(f"Error downloading filing: {e}")
            return None

    def fetch_company_filings(self, ticker: str, filing_type: str = "10-K", count: int = 3):
        """
        High-level method to fetch and save filings for a ticker.
        """
        cik = self.get_cik(ticker)
        if not cik:
            return
        
        print(f"Fetching {filing_type} filings for {ticker} (CIK: {cik})...")
        filings = self.list_filings(cik, filing_type, limit=count)
        
        downloaded_files = []
        for filing in filings:
            date = filing['filingDate']
            fname = f"{ticker}_{filing_type}_{date}.htm" # Usually text/html
            path = self.download_filing(cik, filing['accessionNumber'], filing['primaryDocument'], fname)
            if path:
                downloaded_files.append(path)
                
        return downloaded_files

if __name__ == "__main__":
    loader = SECLoader()
    # Example usage
    loader.fetch_company_filings("AAPL", "10-K", count=1)
