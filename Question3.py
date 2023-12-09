#!/usr/bin/env python
# coding: utf-8

# In[16]:


get_ipython().system('pip install yfinance')
get_ipython().system('pip install bs4')


# In[17]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[20]:


gmestop=yf.Ticker("GME")


# In[21]:


gme_data=gmestop.history(period="max")


# In[22]:


gme_data.reset_index(inplace=True)
gme_data.head()


# In[ ]:




