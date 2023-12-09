#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[5]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url)
soup = BeautifulSoup(html_data.content, "html.parser")


# In[22]:


rows = soup.find('table', attrs={"class":"historical_data_table table"}).find("tbody").find_all("tr")


# In[62]:


data = []
for row in rows:
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    revenue = revenue.replace(',', '').replace('$', '')
    if revenue.strip() != '':  
        data.append({'Date': date, 'Revenue': revenue})


# In[63]:


tesla_revenue = pd.DataFrame(data)


# In[64]:


tesla_revenue.dropna(inplace=True)
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(',|\$', '') 
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[65]:


print(tesla_revenue.tail())


# In[4]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[2]:


try:
    tesla = yf.Ticker("TSLA")
    tesla_data = tesla.history(period="max")
except Exception as e:
    print("an error has ocurred", e)


# In[5]:


make_graph(tesla_data,tesla_revenue,'Tesla')


# In[ ]:


#We can't make the graph, because the .history method for Tesla is not working correctly, if we try with gamestop
#or with Microsoft like we did in the optional tasks, the method runs correctly.

