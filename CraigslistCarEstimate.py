from bs4 import BeautifulSoup
from urllib.request import urlopen
import matplotlib.pyplot as plt
from scipy import stats
from tkinter import *
import time
from selenium import webdriver

def getAllVehicleListingHTML(make, model, year):
    HTML=[]
    for i in range(0,20):
        num =str(i*120)
        site= "https://dallas.craigslist.org/search/cta?"+"s="+num+"&sort=rel&auto_make_model="+ make+ "+"+model+"+&min_auto_year="+year+"&max_auto_year="+year
        html=urlopen(site)
        soup=BeautifulSoup(html, "lxml")
        postingsHTML= soup.find_all("li", class_="result-row")
        if len(postingsHTML)==0:
            break;
        else:
            HTML=HTML+postingsHTML
    return HTML


def getAllVehicleListingIDs(make, model, year):
    ids=[]
    text=getAllVehicleListingHTML(make, model, year)
    for i in range(0, len(text)-8):
        ids.append(text[i].a["href"])
    print (ids)
    return ids



def getAllVehicleDetails(make, model, year):
    endings=getAllVehicleListingIDs(make, model, year)
    cars=[]
    for ending in endings:
        data=[]
        site="https://dallas.craigslist.com"+ending
        html=urlopen(site)
        soup=BeautifulSoup(html, "lxml")
        price=soup.find("span", class_="price")
        odometerSearch=soup.findAll("span")
        odometer=None
        for i in range(0, len(odometerSearch)):
            if str(odometerSearch[i]).find("odometer")>-1:
                odometer=odometerSearch[i]
                break
        if odometer!=None and price!=None:
            print (price)
            data = [int(str(odometer)[str(odometer).index("b>")+2:str(odometer).index("</b")]),int(str(price)[str(price).index("$")+1: str(price).index("</")])]
            cars.append(data)
    print(cars)
    return cars

def getCraigslistFinal(make,model,year, num):
    arr=getAllVehicleDetails(make,model, year)
    print (arr)
    x=[]
    y=[]
    for i in range(0,len(arr)):
        x.append(arr[i][0])
        y.append(arr[i][1])
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    result=slope*int(num) +intercept
    return result


fields = 'Make', 'Model', 'Year','Mileage'

def fetch(entries):
   make=entries[0].get()
   model=entries[1].get()
   year=entries[2].get()
   mileage=entries[3].get()
   vin=entries[4].get()
   craigs=str("Craigslist Estimate: "+str(getCraigslistFinal(make,model, year, mileage)))

   label.config(text=craigs)



def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append( ent)
   return entries

if __name__ == '__main__':
   root = Tk()
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))
   b1 = Button(root, text='Show',
          command=(lambda e=ents: fetch(e)))
   b1.pack(side=LEFT, padx=5, pady=5)
   b2 = Button(root, text='Quit', command=root.quit)
   b2.pack(side=LEFT, padx=5, pady=5)
   label = Label(root, text="Craigslist estimate:")
   label.pack()

   root.mainloop()
