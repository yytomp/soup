# Import Beautiful Soup
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import openpyxl
import os.path


def my_slave(link, df):
    """My_slave is a slave that takes a URL, finds the number of pages it has
    and iterates thru the page to find all the midashi_word needed and print them out
    to an excel sheet"""
    page = requests.get(link)
    soup = bs(page.text, features="lxml")
    result = soup.find("div", {"id" : "search_result"})
    tables = result.find_all("tr")
    # in the search result, find all the words <tr> tag 
    # contains midashi katsuyo jisho and masu
     
    for every in tables:
        word = every.find("p", {"class" : "midashi_word"})
        masu_result = every.find("td", {"class" : "katsuyo katsuyo_masu_js"})
        jisho_result = every.find("td", {"class" : "katsuyo katsuyo_jisho_js"})
        masu_form = ""
        jisho = ""
        kanji = []
        
        if jisho_result is not None:
            char = jisho_result.find_all("span", {"class" : "char"})
            for each in char:
                jisho += each.getText()
        
        if masu_result is not None:
           char = masu_result.find_all("span", {"class" : "char"})
           for each in char:
               masu_form += each.getText()
        
        if word is not None:
            temp = word.getText()
            if "・" in temp :
                kanji = temp.split("・")
            else:
                kanji.append(temp)
                kanji.append("Null")
        
        if jisho_result is not None and masu_result is not None and word is not None:
            temp_df = pd.DataFrame([[kanji[0], jisho, kanji[1], masu_form]], columns=['Kanji', 'jishuo', 'masu', 'masu_form'])
            df = df.append(temp_df)        
            
    return df  
    
#variables to change manually 
file = "Noun_hei_3.xlsx"
sheet = "3-noun_atama"
URL = "https://www.gavo.t.u-tokyo.ac.jp/ojad/search/index/category:6/accent_type:2/mola:3/sortprefix:accent/narabi1:kata_asc/narabi2:accent_asc/narabi3:mola_asc/yure:visible/curve:invisible/details:invisible/limit:100"
path = "E:\spyder\Python\\" + file  


page = requests.get(URL)
soup = bs(page.text, features="lxml")
paginator = soup.find("div", {"id" : "paginator"})
page_total = len(paginator.find_all("a")) + 1

df = pd.DataFrame(columns=['Kanji', 'jishuo', 'masu', 'masu_form'])

for x in range(1,page_total):
    new_URL = URL + "/page:" + str(x)
    
    df = my_slave(new_URL , df)
 
if(os.path.isfile(path)):
    with pd.ExcelWriter(file, mode="a") as writer:
        df.to_excel(writer, sheet_name=sheet)
else:
    with pd.ExcelWriter(file) as writer:
        df.to_excel(writer, sheet_name=sheet)
