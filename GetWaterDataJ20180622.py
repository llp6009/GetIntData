#coding=utf-8
import sys
import threading
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
reload(sys)
import os
import random
sys.setdefaultencoding('utf-8')
from selenium import webdriver
import time
import codecs
import cx_Oracle
from pandas import Series,DataFrame
from lxml import etree
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime,timedelta
from sqlalchemy import *

class GetIP:
    def __init__(self):
        self.URLText=u"http://xxfb.hydroinfo.gov.cn/ssIndex.html?type=2"
        self.browser=webdriver.PhantomJS(r"D:\WORKSOFT\python\Scripts\PhantomJS.exe")
        self.getheaders = DesiredCapabilities.PHANTOMJS.copy()
        self.user_agants = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50', \
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50', \
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;', \
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)', \
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)', \
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1', \
            'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1', \
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)', \
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1', \
            'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1', \
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11', \
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11', \
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11', \
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)', \
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)', \
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)', \
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)', \
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)', \
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)', \
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)', \
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)', \
            ]
        self.headers = {'User_Agant': random.choice(self.user_agants)}

    #def OpenPage(self):#通过模拟浏览器登陆的方式，打开页面
        #r=codecs.open("C:/Users/19535/Desktop/sperdata.txt",'r')
        #lineread=r.read().decode("gbk")
        #return lineread
    def OpenPageNewJS(self):
        self.getheaders["phantomjs.page.settings.userAgent"]=self.headers
        self.getheaders["phantomjs.page.settings.loadImages"] = False
        self.browser.start_session(self.getheaders)
        self.browser.get(self.URLText)
        time.sleep(120)
        html=self.browser.page_source
        self.browser.close()
        return html

    def OpenPageNewN(self):#通过模拟登陆的方式打开浏览器
        PageReturnNum=0#局部变量，浏览器打开次数
        global HtmlStr#全局变量，获取页面信息
        HtmlStr=None
        os.environ["webdriver.ie.IEDriverServer"] = self.browser#调用启动IE浏览器的服务
        driver = webdriver.Ie(self.browser)#打开IE浏览器
        WinBool=True#循环变量，通过
        try:
            while WinBool:
                driver.get(self.URLText)
                time.sleep(120)
                if bool(WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "hdtable")))) == True:
                    HtmlStr = driver.page_source
                    WinBool = False
                    if HtmlStr==None:
                        if PageReturnNum<10:
                            WinBool=True
                            driver.close()
                            PageReturnNum+=1
                        else:
                            WinBool=False
                            print datetime.now,"爬取失败"

                else:
                    if PageReturnNum<10:
                        WinBool = True
                        driver.close()
                        PageReturnNum+=1
                    else:
                        WinBool=False
                        print datetime.now,"爬取失败"
                        self.GetSysTime()
        except:
            print "没有网络，打开页面错误"

        finally:
            driver.quit()
            if bool(HtmlStr):
                return HtmlStr
            else:
                print "爬取数据错误"

    def GetylData(self,x):
        Html=etree.HTML(x)
        getylData01 = Html.xpath(u'//div[@class="ssdiv" and @id="yltable"]/table/tbody/tr/td[1]/text()')
        getylData02 = Html.xpath(u'//div[@class="ssdiv" and @id="yltable"]/table/tbody/tr/td[2]/text()')
        getylData03 = Html.xpath(u'//div[@class="ssdiv" and @id="yltable"]/table/tbody/tr/td[3]/text()')
        getylData04 = Html.xpath(u'//div[@class="ssdiv" and @id="yltable"]/table/tbody/tr/td[4]/text()')
        getylData05 = Html.xpath(u'//div[@class="ssdiv" and @id="yltable"]/table/tbody/tr/td[5]/text()')
        getylData06 = Html.xpath(u'//div[@class="ssdiv" and @id="yltable"]/table/tbody/tr/td[6]/text()')
        getylData07 = Html.xpath(u'//div[@class="ssdiv" and @id="yltable"]/table/tbody/tr/td[7]/text()')
        listnum0=[datetime.now().strftime('%y%m%d')+"01"+str(n) for n in range(1,len(getylData01)+1)]
        listnum1 = [n for n in getylData01]
        listnum2 = [n for n in getylData02]
        listnum3 = [n for n in getylData03]
        listnum4 = [n for n in getylData04]
        listnum5 = [n for n in getylData05]
        listnum6 = [n for n in getylData06]
        listnum7 = [n for n in getylData07]
        data = { 'ID':listnum0,'WRZ_NM': listnum1, 'PROV_NM': listnum2, 'RV_NM': listnum3, 'ST_NM': listnum4, 'ST_TIME': listnum5,
                'DAY_YL': listnum6, 'WEATHER': listnum7}#,'CREATE_TIME': datetime.now().strftime('%y/%m/%d')
        df = DataFrame(data)
        return df

    def GetskData(self, x):#水库
        Html = etree.HTML(x)
        getylData01 = Html.xpath(u'//div[@class="ssdiv" and @id="sktable"]/table/tbody/tr/td[1]/text()')
        getylData02 = Html.xpath(u'//div[@class="ssdiv" and @id="sktable"]/table/tbody/tr/td[2]/text()')
        getylData03 = Html.xpath(u'//div[@class="ssdiv" and @id="sktable"]/table/tbody/tr/td[3]/text()')
        getylData04 = Html.xpath(u'//div[@class="ssdiv" and @id="sktable"]/table/tbody/tr/td[4]/font/text()')
        getylData05 = Html.xpath(u'//div[@class="ssdiv" and @id="sktable"]/table/tbody/tr/td[5]/font/text()')
        getylData06 = Html.xpath(u'//div[@class="ssdiv" and @id="sktable"]/table/tbody/tr/td[6]/text()')
        getylData07 = Html.xpath(u'//div[@class="ssdiv" and @id="sktable"]/table/tbody/tr/td[7]/text()')
        getylData08 = Html.xpath(u'//div[@class="ssdiv" and @id="sktable"]/table/tbody/tr/td[8]/text()')
        listnum0 = [datetime.now().strftime('%y%m%d') + "02" + str(n) for n in range(1, len(getylData01) + 1)]
        listnum1 = [n.replace(u'\xa0', u' ') for n in getylData01]
        listnum2 = [n.replace(u'\xa0', u' ') for n in getylData02]
        listnum3 = [n.replace(u'\xa0', u' ') for n in getylData03]
        listnum4 = [n.replace(u'\xa0', u' ') for n in getylData04]
        listnum5 = [n.replace(u'\xa0', u' ') for n in getylData05]
        listnum6 = [n.replace(u'\xa0', u' ') for n in getylData06]
        listnum7 = [n.replace(u'\xa0', u' ') for n in getylData07]
        listnum8 = [n.replace(u'\xa0', u' ') for n in getylData08]
        data = {'ID':listnum0,'WRZ_CD':'Null','WRZ_NM': listnum1, 'RV_CD':'Null','RV_NM': listnum2,'RES_ID':'Null', 'RES_NM': listnum3, 'PROV_CD': 'Null','PROV_NM': listnum4, 'RES_Z': listnum5,
                'RES_W': listnum6, 'IN_RES': listnum7,'CREATE_TIME': datetime.now().strftime('%y/%m/%d'),'RES_ALT':listnum8}
        df = DataFrame(data)
        return df

    def GethdData(self, x):
        Html = etree.HTML(x)
        getylData01 = Html.xpath(u'//div[@class="ssdiv" and @id="hdtable"]/table/tbody/tr/td[1]/text()')
        getylData02 = Html.xpath(u'//div[@class="ssdiv" and @id="hdtable"]/table/tbody/tr/td[2]/text()')
        getylData03 = Html.xpath(u'//div[@class="ssdiv" and @id="hdtable"]/table/tbody/tr/td[3]/text()')
        getylData04 = Html.xpath(u'//div[@class="ssdiv" and @id="hdtable"]/table/tbody/tr/td[4]/font/text()')
        getylData05 = Html.xpath(u'//div[@class="ssdiv" and @id="hdtable"]/table/tbody/tr/td[5]/text()')
        getylData06 = Html.xpath(u'//div[@class="ssdiv" and @id="hdtable"]/table/tbody/tr/td[6]/font[1]/text()')
        getylData07 = Html.xpath(u'//div[@class="ssdiv" and @id="hdtable"]/table/tbody/tr/td[6]/font[2]/text()')
        getylData08 = Html.xpath(u'//div[@class="ssdiv" and @id="hdtable"]/table/tbody/tr/td[7]/text()')
        getylData09 = Html.xpath(u'//div[@class="ssdiv" and @id="hdtable"]/table/tbody/tr/td[8]/text()')
        listnum0 = [datetime.now().strftime('%y%m%d') + "03" + str(n) for n in range(1, len(getylData01) + 1)]
        listnum1 = [n.replace(u'\xa0', u' ') for n in getylData01]
        listnum2 = [n.replace(u'\xa0', u' ') for n in getylData02]
        listnum3 = [n.replace(u'\xa0', u' ') for n in getylData03]
        listnum4 = [n.replace(u'\xa0', u' ') for n in getylData04]
        listnum5 = [n.replace(u'\xa0', u' ') for n in getylData05]
        listnum6 = [n.replace(u'\xa0', u' ') for n in getylData06]
        listnum7 = [n.replace(u'\xa0', u' ') for n in getylData07]
        listnum8 = [n.replace(u'\xa0', u' ') for n in getylData08]
        listnum9 = [n.replace(u'\xa0', u' ') for n in getylData09]
        data = {'ID':listnum0,'PROV_CD':'Null','PROV_NM': listnum1,'RV_CD':'Null','RV_NM': listnum2, 'ST_CD':'Null','ST_NM': listnum3,'WRZ_CD':'Null', 'WRZ_NM': listnum4, 'ST_TIME': listnum5,
                'SW_Z': listnum6, 'SW_Q': listnum7, 'SW_M': listnum8, 'WARN_Z': listnum9,'CREATE_TIME': datetime.now().strftime('%y/%m/%d')}
        df = DataFrame(data)
        return df

    def AllIn(self):
        Error = open('ErrorLog.txt', 'a')
        ErrorCount = 0
        x=create_engine("数据库地址", echo=False)
        while true:
            try:
                PageSource = self.OpenPageNewJS()
                yl = self.GetylData(PageSource)
                sk = self.GetskData(PageSource)
                hd = self.GethdData(PageSource)


                if yl.all==0:
                    yl = self.GetylData(PageSource)
                if sk.all==0:
                    sk = self.GetskData(PageSource)
                if hd.all==0:
                    hd = self.GethdData(PageSource)


                print sk.count()
                sk.to_sql(con=x,schema='water_knowledge_new',if_exists='append',name='WR_DXSK_SQ2',index=False,chunksize=100)
                sk.to_excel(str(datetime.now().date()) + "GetSKData.xlsx")

                print hd.count()
                hd.to_sql(con=x,schema='water_knowledge_new',if_exists='append',name='WR_DJDH_SQ2',index=False,chunksize=100)#WR_DJDH_SQ2
                hd.to_excel(str(datetime.now().date()) + "GetHDData.xlsx")

                print yl.count()
                yl.to_sql(con=x,schema='water_knowledge_new',if_exists='append',name='WR_ZDSYQ2',index=False,chunksize=100)
                yl.to_excel(str(datetime.now().date())+"GetYlData.xlsx")

                Error.close()
                break
            except Exception,e:
                strError = str(datetime.now()) + '----' + str(Exception) + '----' + str(e)
                if ErrorCount == 3:
                    Error.writelines(strError + '\n')
                    Error.close()
                    break
                ErrorCount = ErrorCount + 1
                Error.writelines(strError + '\n')
                print strError
                time.sleep(3)

        # PageSource=self.OpenPageNewN()

    def GetSysTime(self):
        datatime=datetime.now()
        destime=datatime.replace(hour=12,minute=0,second=0,microsecond=0)
        delta=destime-datatime
        x=int(delta.total_seconds())
        if x>660 :
            print "-----Plan1----"
            print datetime.now()
            t=threading.Timer(600,self.GetSysTime)
            t.start()
        elif x>120 and x<=660:
            print "-----Plan2----"
            print datetime.now()
            t=threading.Timer(90,self.GetSysTime)
            t.start()
        elif x>0 and x<=120:
            print "-----Plan3----"
            print datetime.now()
            self.AllIn()
            t=threading.Timer(36000,self.GetSysTime)
            t.start()
        else:
            print "-----Plan4----"
            print datetime.now()
            t=threading.Timer(18000,self.GetSysTime)
            t.start()

if __name__ == '__main__':
    getpage = GetIP()
    # getpage.AllIn()
    getpage.GetSysTime()






