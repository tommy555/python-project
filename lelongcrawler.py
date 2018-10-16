import requests
from bs4 import BeautifulSoup as bs
from random import randint

header = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"
}

url = "https://www.lelong.com.my/catalog/all/list"
timeout = randint(80, 180)
param = {
    "TheKeyword" : "Nvidia GTX 1070"
}
responses = requests.get(url, params = param, headers = header, timeout = timeout)

soup = bs(responses.text, "html.parser")

f = open("responses.txt", 'w')

for items in soup.find_all("img"):
    dataName = items.get("data-name")
    dataPrice = items.get("data-price")
    dataLink = items.get("data-link")

    if dataName != None and  dataPrice != None and dataLink != None:
        itemDesc = "Item name: {}\nItem price: {}\nItem link: {}\n\n".format(dataName , dataPrice, dataLink)
        f.write(itemDesc)

f.close()

print("Done")