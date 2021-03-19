# In []:

import pandas as pd
import requests
from lxml import etree
import re
# import collections
import numpy as np


# In []
sample = '15000' #Number of samples
sc = '6yzf' # Sort key
st = 'desc' # Sort by
ft = 'gp' #Fund type
dx = '1' #Is it available
season = 1 #Select quarter


rlx = 1 # Daily growth rate
rlz = 1 # Since a week
rly = 1 # Since this months
r3y = 0.3333 #Since the past 3 months
r6y = 0.3333 #Since the past 6 months
r1n = 0.25 #In the past 1 year
r2n = 0.25 #In the past 2 years
r3n = 0.25 # In the past 3 years
rjnl = 0.25 #Since this year
rcll = 1 #Since it is founded




sd = '2021-01-07'
ed = '2021-02-07'

# In[]
# from PyQt5.QtWidgest import QDialog
from PyQt5.QtWidgets import QDialog
import sys
from PyQt5. QtWidgets import
import dialog
class TestDialog1(QDialod, dialog.Ui_XMtool):
    def _init_(self.parent=None)：
        super (TestDialog1, self)._init_(parent)
        self.setupUi(self)

    app = QApplication(sys.argv)
    dig = TestDialog1()
    dlg.show()
    app.exec_()

    sample = dlg.sample.text() #Number of samples
    sc = dlg.sc.currentText() #Sort key
    st = dlg.st.currentText() #Sort by
    ft = dlg.ft.currentText() #Fund type
    dx = dlg.dx.currentText() #Is it available
    season = int(dlg.season.surrentText()) #Select quarter


r1r = float(dlg.r1r.text()) #Daily growth rate
r1z = float(dlg.r1z.text()) #Since a week
r1y = float(dlg.r1y.text()) #Since this months
r3y =  float(dlg.r3y.text()) #Since the past 3 months
r6y =  float(dlg.r6y.text()) #Since the past 6 months
r1n =  float(dlg.r1n.text()) #In the past 1 year
r2n =  float(dlg.r2n.text()) #In the past 2 year
r3n =  float(dlg.r3n.text()) #In the past 3 year
rjnl =  float(dlg.rjnl.text()) #Since this year
rcll =  float(dlg.rcll.text()) #Since it is founded
# In[]:
header = {
         'User-Agent': 'Mozilla/5.0(Window NT 10.0 ; Win 64 ; x64) AppleWebKit/537.36(KHTML , like Gecko) Chrome/88.0.4324.96 Safari/537.36',
         'Referer' : 'http://fund.eastmoney.com/data/fundranking.html',
         'Cookie' : 'st_si = 74949607860286: st_asi=delete: ASP.NET_SessionId=gekyucn.......' #Unfinished
}
url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt= '+ft+' &rs=&gs=0&sc= '+sc+' &st='+st+' &sd= '+sd+' &ed= '+ed+' &qdii=&tabSubtype= ,,,,, &pi = 1&pn='+sample+' &dx= '+dx+' &v=0.2692835962833908'
response = requests.get(url=url, headers=header)
text = response.text
data = text. split('=')[1]
compile_data = re.findall("{datas: \\[(.*)\\], allRecords", str(data))[0] # Get all the content in datas and allRecords
strip_data = sstr(compile_data).strip('[').strip(']') #Remove the brackets at the beginning and end of the string
replace_quta = strip_data.replace('"', "")#Replace double quotes with empty
quota_arrays = replace_quta.split(",") # Use comma to convert to list
intervals = [[i * 25, (i + 1) * 25] for i in range(15000)] #Generate 10,000 intervals, each with a length of 25
narrays = []
for k in intervals:
    start, end = k[0], k[1]
    line = quota_arrays[start: end] # Group item 25 into a group to indicate a fund
    narrays.append(line)
header= ["基金代码", "基金简称", "基金条码", "日期", "单位净值","累计净值","日增长率", "近1周","近1月","近3月“，"近半年", "近1年","近2年","近3年",
         "今年来" ,"成立来" ,"其他1" ,"其他2", "其他3" , "其他4" ,"其他5 , "其他6" , "其他7" , "其他8" , "其他9"]
df = pd.DataFrame(narrays, columns = header) #Generate pd data structure
df.dropna()
total = df.count()[0]
print("There are {} funds!" .format(total))
df = df.head(total)
df_part = df[["基金代码", "基金简称", "基金条码", "日期", "单位净值","累计净值","日增长率", "近1周","近1月","近3月“，"近半年", "近1年","近2年","近3年",
         "今年来" ,"成立来"]] #挑选部分感兴趣的条目
df. to_csv("./基金增长率.csv", encoding= "utf_8_sig")


# In[]:
df_picked_part = df_part
rates = [rlr,rlz,rly,r3y,r6y,rln,r2n,r3n,rjn1,rcll]
i= -1
for sc in ["日增长率", "近1周","近1月","近3月“，"近半年", "近1年","近2年","近3年","今年来","成立来"]:
    i = i+1
    #print(sc)

    rate = rates[i]
    rate_num = int(total*rate)
    df_tmp = df_part.sort_values(by=[sc], ascending = False, axis = 0)
    df_temp = df_temp.head(rate_num)
    df_picked_part = pd.merge(df_picked_part, df_temp,how='inner')
print(df_picked_part .head(10))
df_picked_part.to_csv("./4433法则结果.csv", encoding= "utf_8_sig")

# In[]:
rank_codes = df_part['基金代码'].values.tolist()
#len.codes = len(rank.codes)
stocks_array = []
stock_funds = []
total_part = int（total/100)+1 #Report progress every half
for index, code in enumerate(rank_codes):
#    if index < 1:
#         print("<" * 30 + "Top 10 stock pools of all funds" + ">" * 30)
#    print(code)
    if index%total_part == 0 :
        print("<" * 30 + "Obtaining fund holding data:" + str(index)+ "/" +str(total)+ ">" * 30)
    url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type = jjcc&code={} &topline=10&year=&month=&rt=0.5032668912422176"
    head = {
    "Cookie":

    "User-Agent":
     }
    response = requests.get（url. headers = head)
    text = response.text
    div = re.findall('content :\\"(.*)\\',arryear', text)[0]
    html_body = '<! DOCTYPE html lang="en"><head><neta charset="UTF-8"><title></head><body>%s</body></html>'%(
        div) #Construct a web page
    stock_info = html.xpath('//div[{}]/div/table/tbody/tr/td/a' .format(season))
    #for li in stock.info:
    #    print(li.text)
    #print(season)
    stock_money = html.xpath('//div[{}]/div/table/tbody/tr/td[@calss="tor"]' .format(season))
    if stock_money == []:
        stock_money = html.xpath('.//div[{}]/div/table/tbody/tr/td[@calss="tor"]' .format(season))
    stock_attr =[]
    # for i in range(0, len(stock_money)]:

    stock_money_text = []
    for li in stock_money:
        li_text = li.text
            print(li_text)
        if li_text!=None:
            li.text = li.text.replace('---' , '0')
            stock_money_text.append(float(li.text.replace(',', ''). replace('%', '')))

    #   print(li.text)
    #stock_money_text.dropna()
    stock_one_fund =[]
    if len(stock_info)!=0 and len(stock_money_text) !=0:
        count = -1
        for i in range(0,len(stock_info)):
            stock = stock_info[i]
            if stock.text == Nome:
                stock.text = '缺失'
            temp0 = stock.text.split('.')
            temp = temp0[0]
            if stock.text and (temp.isdiggit() or (temp.isupper() and temp. isalnum() and len(temp0)>1)):
    #           if stock.text and stock.text.isdigit():
                    #list_temp = [stock.text, stock_info[i+1].text]
                count =count+1
                stock_one_fund.append([stock_info[i+1],
                                       stock_money_text[3*count+0],
                                       stock_money_text[3*count+1],
                                       stock_money_text[3*count+2]])

        stock_funds.append([code,stock_one_fund])

        stocks_array.extend(stock_one_fund)
    print("<" * 30 +"Obtaining fund holding data ： done!!! " +">" *30)
    #print("test")
    temp = pd.DataFrame(stock_funds, columns=["基金代码"，"十大重仓"])
    df_funds_info_extend = pd.merge(df_part, temp, how="inner", on="基金代码")
    df_funds_info_extend.set_index("基金代码")
    df_funds_info_extend.to_csv("./基金持仓.csv",encoding="utf_8_sig")


    #In[]:
    stock_info_list =[]
    for row in df_funds_info_extend.iterrows():
        tenpos = row[1]["十大重仓"]
        fund_jc = row[1]["基金简称"]
        if len(tenpos)!=0:
            temp = [tenpos[0][0], fund_jc, tenpos[0][1], tenpos[0][2],tenpos[0][3]]
            stock_info_list.append(temp)
    df_stock_info = pd.DataFrame(stock_info_list,columns=["股票简称", "所属基金", "占净值比例","持股数_万"， "持仓数_万"])
    df_stock_info.to_csv("./股票被持有信息.csv", encoding="utf_8_sig")

    #In[]

    df_stock_info_cp = df_stock_info
    df_stock_info_cp["所属基金cp"]= df_stock_info["所属基金"]
    df_stock_info_gb = df_stock_info_cp.groupby("股票简称")





    stock_agg_result= df_stock_info_gb.agg({"持股数_万": np.sum."持股市值_万": np.sum, "占净值比例": np.mean, "所属基金":len,"所属基金cp":list})
    stock_agg_result.columns = ["被持股数_万", "被持仓市值_万","平均占比", "所属基金数目", "所属基金组合"]
    stock_agg_result.to_csv("./股票被持有信息统计.csv", encoding="utf_g_sig")


    #In[]
    rank = 10
    stock_agg_result = stock_agg_result.sort_values(by="所属基金数目",ascending=False)
    stock_agg_result_head0 = stock_agg_result_head(rank)
    stock_agg_result = stock_agg_result.sort_values(by="被持仓市值_万", ascending=False)
    stock_agg_result_head1 = stock_agg_result_head(rank)
    stock_agg_result = stock_agg_result.sort_values(by+"平均占比"，ascending=False)
    stock_agg_result_head2 = stock_agg_result_head(rank)
    funds_stocks_count =[]
    for st_fund_ in stock_funds:

        st_funds = st_funds_[1]
        temp = [i[0] for i in st_funds]
        df_stock_funds = pd.DataFrame(temp,columns=["股票简称"])

        count0 = pd.merge(stock_egg_result_head0, df_stock_funds, how="inner", on="股票简称").iloc[:,0].size
        count1 = pd.merge(stock_egg_result_head1, df_stock_funds, how="inner", on="股票简称").iloc[:, 0].size
        count2 = pd.merge(stock_egg_result_head2, df_stock_funds, how="inner", on="股票简称").iloc[:, 0].size
        jc_temp = df_part[df_part["基金代码"]==st_funds_[0]].iloc[0,1]
        funds_stocks_count.append([jc_temp,count0,count1,count2])
    df_funds_stock_count = pd.DataFrame(funds_stocks_count, columns = ["基金简称","优仓数目_所属基金数"，"优仓数目_被持仓市值"，"平均占比"])
    df_funds_stock_count = df_funds_stock_count.sort_values(by=["优仓数目_所属基金数"]，ascending=False, axis=0)
    df_funds_stock_count = pd.merge(df_funds_stock_count,df_part,how="inner", on="基金简称")
    df_funds_stock_count.to_csv("./基金持受欢迎股数目统计.csv", encoding="utf_8_sig")





    }


