#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install yfinance')
get_ipython().system('pip install bs4')


# In[3]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[9]:


url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data=requests.get(url)
soup=BeautifulSoup(html_data.content,"html.parser")


# In[10]:


rows = soup.find('table', attrs={"class":"historical_data_table table"}).find("tbody").find_all("tr")


# In[11]:


data = []
for row in rows:
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    revenue = revenue.replace(',', '').replace('$', '')
    if revenue.strip() != '':  
        data.append({'Date': date, 'Revenue': revenue})


# In[12]:


gme_revenue = pd.DataFrame(data)


# In[13]:


gme_revenue.dropna(inplace=True)
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(',|\$', '') 
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]


# In[14]:


print(gme_revenue.tail())


# In[15]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[18]:


gmestop=yf.Ticker("GME")
gme_data=gmestop.history(period="max")
gme_data.reset_index(inplace=True)


# In[19]:


make_graph(gme_data,gme_revenue,'GameStop')


# In[ ]:




