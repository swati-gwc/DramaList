import requests
from bs4 import BeautifulSoup
import csv
import re

ids=[]
for i in range(1,251):
    URL = "https://mydramalist.com/shows?page=%s" % i
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    content = soup.find('div', attrs = {'class':'m-t nav-active-border b-primary'})
    for subcontent in content.findAll('div', attrs = {'class':'col-xs-9 row-cell content'}):
        # title = subcontent.h6.text
        # title = title.replace('\'','')
        # if '&' in title:
        #     pos = title.index('&')
        #     if(title[pos-1]==' '):
        #         title = title.replace(title[pos-1],'')
        # title = title.replace('&','-')
        urlpath=''
        for link in subcontent.h6.find_all('a', attrs={'href': re.compile("^/")}):
            urlpath = link.get('href')
            #ids.append(link.get('href'))  
       
        #title = title.lower().strip()
        for item in subcontent.find_all(attrs={"data-stats": True}):
             if 'mylist' in item['data-stats']:
                #   idd = item['data-id'] + ' ' + title
                #   idd = idd.replace(' ','-') 
                urlpath = urlpath[1:]
                ids.append(urlpath)

#print(ids)

dramadata = []

for list in ids:      
    URL2 = "https://mydramalist.com/%s" %list
    #print(URL2)
    page2 = requests.get(URL2)
    soup2 = BeautifulSoup(page2.content, "html.parser")
    subdata={}

    subdata['url']=URL2
    subdata['id']= list.split('-',1)[0].replace('/','')

    # findtitle = soup2.find('div', attrs = {'class':'box-header box-navbar mdl-component'})    
    # collecttitle=findtitle.find('h1', attrs = {'class':'film-title'})
    # subdata['title'] = collecttitle.text
    for row in soup2.findAll('h1', attrs = {'class':'film-title'}):
        subdata['title'] = row.text

    #dramainfo = soup2.find('li', attrs = {'class':'list-item p-a-0'}) 
    for row in soup2.findAll('li', attrs = {'class':'list-item p-a-0 show-genres'}):
        subdata['genres']=row.text.split(':',1)[1].replace(' ','')
        #print(subdata)     

    for row in soup2.findAll('li', attrs = {'class':'list-item p-a-0 show-tags'}):
        tagdata = row.text.split(':',1)[1].replace(' ','')
        subdata['tags']= tagdata.replace('(Voteoraddtags)','')
        # print(subdata)  
    #(Voteoraddtags) remove it from tags :TASK PENDING
    attributes = ['type','country','director','alsoknownas','episodes','score','aired','duration']
    for row in soup2.findAll('li', attrs = {'class':'list-item p-a-0'}):
        subdataKey = row.text.split(':')[0].replace(' ','').lower()
        subdataValue = row.text.split(':',1)[1]
        if subdataKey in attributes:
            subdata[subdataKey]=subdataValue
            #print(subdataKey,subdataValue)  

    #actorInfo = soup2.find('div', attrs = {'class':'col-lg-8 col-md-8 col-right'}) 
    #actorInfo = soup2.find('div', attrs = {'class':'list-item col-sm-4'}) 
    actormainrole = ""
    actorsupportrole = ""
    for row in soup2.findAll('li', attrs = {'class':'list-item col-sm-4'}):
        actorRoletype = row.find('small', attrs = {'class':'text-muted'}) 
        if(actorRoletype.text == 'Main Role'):
            actortitle = row.find('a', attrs = {'class':'text-primary text-ellipsis'}) 
            #print(actortitle.text)
            actormainrole+=actortitle.text+","    
            subdata['mainrole']=actormainrole 
        elif(actorRoletype.text == 'Support Role'):
            actortitle = row.find('a', attrs = {'class':'text-primary text-ellipsis'}) 
            #print(actortitle.text)
            actorsupportrole+=actortitle.text+","
            subdata['supportrole']=actorsupportrole 
        

        #print(row.text)

    # print(actorInfo)

    dramadata.append(subdata)

import csv
import io
filename = 'mydramalist.csv'
with io.open(filename, 'w+', newline='',encoding="utf-8") as f:
    w = csv.DictWriter(f,['id','url','title','type','country','director','alsoknownas','episodes','score','aired','duration','genres','tags','mainrole','supportrole'])
    w.writeheader()
    for dramasubdata in dramadata:
        w.writerow(dramasubdata)
