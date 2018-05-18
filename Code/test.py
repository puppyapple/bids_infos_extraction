''''' 
Created on 2016年8月27日 
 
@author: Administrator 
'''  
import urllib  
import urllib.request  
from bs4 import BeautifulSoup  
from User import *  
import os
import pandas as pd

class GetUserListByBS4():  
  
    def __init__(self):  
        self.user=User()  
        ''''' 
        Constructor 
        '''  
    def get(self,url,coding):  
        req=urllib.request.Request(url)  
        response=urllib.request.urlopen(req)  
        htmls=response.read()  
        htm=htmls.decode(coding,'ignore')  
        return htm  
          
if __name__=="__main__":  
    get=GetUserListByBS4()  
    # html=get.get("https://www.baidu.com/", "utf-8") 
    html = open("../Data/Input/bids_infos_extraction/test.html").read()
    print(html)
    soup=BeautifulSoup(html,"html.parser")  
    trs=soup.find_all(name='tr', attrs={'class':"tr"})  
    userList=list()  
    for tr in trs:  
        user=User()  
        _soup=BeautifulSoup(str(tr),"html.parser")  
        tds=_soup.find_all(name='td')  
        _id=_soup.input['id']  
        user.setId(_id)  
        user.setName(str(tds[1].string))  
        user.setAge(str(tds[2].string))  
        userList.append(user)  
      
    for i in userList:  
        print(i)  

    a = pd.read_html("../Data/Input/bids_infos_extraction/test.html")
    print(a)