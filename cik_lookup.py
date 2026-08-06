import requests

class SecEdgar:
    def __init__(self, fileurl):
        self.fileurl = fileurl

        self.headers = {
            "User-Agent": "Esohe Osaghae esoheosaghae26@gmail.com"
        }

    def name_to_cik(self, name):
        response = requests.get(self.fileurl, headers=self.headers)

        data = response.json()

        # Return a tuple of CIK, Name, Ticker
        for company in data.values():
            if company["title"] == name:
                return (
                    company["cik_str"],
                    company["title"],
                    company["ticker"]
                )
                                

    def ticker_to_cik(self, ticker):
        response = requests.get(self.fileurl, headers=self.headers)

        data = response.json()

        # Return a tuple of CIK, Name, Ticker
        for company in data.values():
            if company["ticker"] == ticker:
                return (
                    company["cik_str"],
                    company["title"],
                    company["ticker"]
                )

sec = SecEdgar("https://www.sec.gov/files/company_tickers.json")