import pandas as pd
import datetime
from bs4 import BeautifulSoup
import requests

class MagicFormula:

    def __init__(self):
        self.desc = "Class is MagicFormula for stocks data retrieval from the MagiFormula website."

    def get_stocks(self, email, password, minMarketCap=100, stocksNum=30, compression=None):
        ##############################
        #### magicformula website ####
        ##############################
        tries = 0
        while tries < 5:
            try:
                # to login into page, first 'get' page to get cookie, then 'post' to sign in
                s = requests.Session()
                url1 = "https://www.magicformulainvesting.com/Account/LogOn"
                r1 = s.get(url1)

                # Check for correct email and password entered
                if email == '':
                    raise Exception('Email is invalid or missing.')
                if password == '':
                    raise Exception('Password is invalid or missing.')

                login_data = {"Email": email, "Password": password, "login": "Login"}
                r1 = s.post(url1, data=login_data, headers={"Referer": "https://www.magicformulainvesting.com/"})

                # Get the stocks data
                url2 = "https://www.magicformulainvesting.com/Screening/StockScreening"
                if stocksNum == 30:
                    select30 = "true"
                else:
                    select30 = "false"

                payload = {"MinimumMarketCap": minMarketCap, "Select30": select30, "stocks": "Get+Stocks"}
                r2 = s.post(url2, data=payload)
                soup = BeautifulSoup(r2.text, "html.parser")
                results = soup.find("div", {"id": "report"}).find("tbody").find_all("tr")
                numrows = len(results)

                # create dataframe with initial data out of magicformula website
                df = pd.DataFrame(index=range(numrows),
                                  columns=list(['Company Name',         # 0
                                                'Ticker',               # 1
                                                'Market Cap ($Mlns)',   # 2
                                                'Price From',           # 3
                                                'Most Recent Quarter Data']))  # 4
                j = 0
                for item in results:
                   i = 0
                   name = item.find_all("td")
                   while i < len(name):
                       df.iloc[[j], [i]] = name[i].text
                       i += 1
                   j += 1
                print("MagicFormula basic data complete")
                break
            except:
                tries=+1
                if tries==5: raise Exception("Uknown problem encountered: could be internet or server-side issue. "
                                             "Please try again.")

        ##########################################
        ### Saving the dataframe to a csv file ###
        ##########################################

        now = datetime.datetime.now()
        dateversion = now.strftime("%Y-%m-%d")
        filename = '.\MagicFormulaStocks_MarketCap' + str(minMarketCap) + '_' + str(dateversion) + '.csv'
        df.to_csv(path_or_buf=filename, mode='w+', compression=compression)
        print("MagicFormula stocks data retrieval complete.")
        return df, filename