#code based on https://www.freecodecamp.org/news/scraping-ecommerce-website-with-python/
import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.jumia.co.ke/"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
productlinks = []
t={}
data=[]
c=0
for x in range(1,6):
    k = requests.get('https://www.jumia.co.ke/phones-tablets/?page={}#catalog-listing'.format(x)).text
    soup=BeautifulSoup(k,'html.parser')
    productlist = soup.find_all("article",{"class":"prd _fb col c-prd"})


    for product in productlist:
        link = product.find("a",{"class":"core"}).get('href')
        productlinks.append(baseurl + link)


for link in productlinks:
    f = requests.get(link,headers=headers).text
    hun=BeautifulSoup(f,'html.parser')

    try:
        price=hun.find("span",{"class":"-b -ubpt -tal -fs24 -prxs"}).text.replace('\n',"")
    except:
        price = None

    try:
        about=hun.find("h1",{"class":"-fs20"}).text.replace('\n',"")
        
    except:
        about=None


    try:
        rating = hun.find("div",{"class":"stars"}).text.replace('\n',"")
    except:
        rating=None

    try:
        namearr=hun.find("h1",{"class":"-fs20"}).text.replace('\n',"").split()[0:3]
        name = ' '.join(namearr)
    except:
        name=None

    phones_tablets = {"name":name,"about":about,"price":price,"rating":rating} 

    data.append(phones_tablets)
    c=c+1
    print("completed",c)

df = pd.DataFrame(data)
df.to_excel("output.xlsx")  



