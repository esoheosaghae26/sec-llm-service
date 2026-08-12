import requests

class SecEdgar:
    def __init__(self, fileurl):
        # I have been using this url: https://www.sec.gov/files/company_tickers.json

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

    def annual_filing(self, cik, year): # 10-K
        submissions = self.__get_submissions(cik)
        recent = submissions["filings"]["recent"]

        for i in range(len(recent["form"])):
            if recent["form"][i] == "10-K":
                if recent["filingDate"][i].startswith(str(year)):
                    return self.__build_document_url(
                        cik,
                        recent["accessionNumber"][i],
                        recent["primaryDocument"][i]
                    )

    def quarterly_filing(self, cik, year, quarter): # 10-Q
        if quarter not in [1, 2, 3]:
            raise ValueError("Quarter must be 1, 2, or 3")

        submissions = self.__get_submissions(cik)
        recent = submissions["filings"]["recent"]
        quarterly_filings = []
        
        for i in range(len(recent["form"])):
            if recent["form"][i] == "10-Q":
                if recent["filingDate"][i].startswith(str(year)):
                    quarterly_filings.append(i)

        if len(quarterly_filings) < quarter:
            raise ValueError(f"No 10-Q found for Q{quarter} of {year}")

        quarterly_filings.reverse()

        index = quarterly_filings[quarter - 1]

        return self.__build_document_url(
            cik,
            recent["accessionNumber"][index],
            recent["primaryDocument"][index]
        )

    def __get_submissions(self, cik):
        cik = str(cik).zfill(10)

        url = f"https://data.sec.gov/submissions/CIK{cik}.json"

        response = requests.get(url, headers=self.headers)

        return response.json()

    def __build_document_url(self, cik, accession_number, primary_document):
        cik = str(cik).zfill(10)
        accession_number = accession_number.replace("-", "")

        return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{primary_document}"