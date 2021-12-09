import pandas as pd
import requests
import concurrent.futures
import gspread
from google.oauth2.service_account import Credentials
from bs4 import BeautifulSoup, SoupStrainer
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

MAX_THREADS = 20 #Set maximum number of threads

#Define retry conditions in case of network exception
session = requests.Session()
retry = Retry(total=3, backoff_factor=0.1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

#Access Google service account authentication
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file(
    './serviceAccountKey.json',
    scopes=scopes
)
gc = gspread.authorize(credentials)

df1 = pd.read_excel("URL's.xlsx", "URL") #Read excel file and store in a dataframe

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'} #Define headers for accessing the website

urlList = []
urlListTemp = []
productNameList = []
productBrandList = []
offerList = []
productPriceList = []
salePriceList = []
availabilityList = []
productCodeList = []

strainer = SoupStrainer(id="productRight") #Define what part the program will scrape

#Update worksheet
def update_sheet():
        sh = gc.open_by_key('10NQXE9iovumhJN5kd9jPrfQAMQWMH_ir_hs7Wwb8Zak')#Worksheet key
        #Clear and export df2 values to the first sheet
        worksheet = sh.get_worksheet(0)
        worksheet.clear()
        df2ws = df2.values.tolist()
        worksheet.update(df2ws)

def crawl(z):
        page = requests.get(z, headers=headers)#Get page
        soup = BeautifulSoup(page.content, "lxml", parse_only=strainer)#Get the relevant part of soup
        try:#Try to find price informaiton
                #Get the information from the page
                productPrice = soup.find('span', {"class": "product-price"}).get_text()
                productBrandTemp = soup.find('span', {"class": "fbold"}).get_text()
                productBrand = productBrandTemp.replace(' ', '')
                productNameTemp = soup.find(id="product-name").get_text()
                productName = productNameTemp.replace(productBrandTemp, '')
                salePrice = soup.find('span', {"class": "product-price"}).get_text()
                offer = soup.find('div', {"class": "detay-indirim"}).get_text()
                variant = soup.find('div', {'class': 'new-size-variant fl col-12 ease variantList'})
                variantChild = list(variant.findChildren('a', recursive=False))
                unavailable = soup.findAll('a', {'class': 'col box-border passive'})
                availability = (1-(round(len(unavailable)/len(variantChild), 4))) * 100
                avaStr = str("%.2f" % availability) + "%"
                description = list(soup.find('div', {'class': 'product-feature-content'}))
                #Add the information to the relevant lists
                productNameList.append(productName.strip())
                productBrandList.append(productBrand.strip())
                offerList.append(offer.strip())
                productPriceList.append(productPrice.strip())
                salePriceList.append(salePrice.strip())
                availabilityList.append(avaStr)
                urlList.append(z)
                #Check to see if last item in description is a product code
                if ('.' in description[-1].strip()) == True:
                        if (' ' in description[-1].strip()) == True:
                                productCodeList.append("-")
                        else:
                                productCodeList.append(description[-1].strip())
                else:
                        if (' ' in description[-2].strip()) == True:
                                productCodeList.append("-")
                        else:
                                productCodeList.append(description[-2].strip())

        except:#If no price information
                try:#Try to find other information, the item is out of stock
                        productBrandTemp = soup.find('span', {"class": "fbold"}).get_text()
                        productBrand = productBrandTemp.replace(' ', '')
                        productNameTemp = soup.find(id="product-name").get_text()
                        productName = productNameTemp.replace(productBrandTemp, '')
                        description = list(soup.find('div', {'class': 'product-feature-content'}))
                        #Add the information to the relevant lists
                        productNameList.append(productName.strip())
                        productBrandList.append(productBrand.strip())
                        offerList.append("-")
                        productPriceList.append("-")
                        salePriceList.append("-")
                        availabilityList.append("0.0%")
                        urlList.append(z)
                        # Check to see if last item in description is a product code
                        if ('.' in description[-1].strip()) == True:
                                if (' ' in description[-1].strip()) == True:
                                        productCodeList.append("-")
                                else:
                                        productCodeList.append(description[-1].strip())
                        else:
                                if (' ' in description[-2].strip()) == True:
                                        productCodeList.append("-")
                                else:
                                        productCodeList.append(description[-2].strip())

                except:#If no information is found
                        pass#Disregard the exception


def main():
        #Create list with all URL's
        for n in range(0,len(df1.index)):
                url = 'http://www.markastok.com' + df1.iloc[n, 0]
                urlListTemp.append(url)
        #Set number of threads to minimum of MAX_THREADS or number of URL's
        threads = min(MAX_THREADS, len(urlListTemp))
        #Run crawler with multithreading
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                for url in urlListTemp:
                        executor.submit(crawl, z=url)
        #Convert lists into dataframe
        global df2
        df2 = pd.DataFrame(
                list(zip(urlList, productNameList, productBrandList, offerList, productPriceList, salePriceList,
                         availabilityList, productCodeList)),
                columns=['URL', 'ProductName', 'Brand', 'Offer', 'ProductPrice', 'SalePrice', 'Availability', 'ProductCode'])

        df2.to_excel("ProductReport.xlsx", index=False)#Export dataframe as excel

        update_sheet()#Update google sheet

main()
