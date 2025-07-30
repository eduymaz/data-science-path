# DATA : https://archive.ics.uci.edu/dataset/502/online+retail+ii

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_ = pd.read_excel('../data/online_retail_II.xlsx', sheet_name="Year 2009-2010")
df = df_.copy()
df.head()
df.isnull().sum()

df = df[~df["Invoice"].str.contains("C", na=False)]
df.describe()

df = df[(df["Quantity"]>0)]
df.dropna(inplace=True)

#add to new column "TotalPrice"
df["TotalPrice"] = df["Quantity"] * df["Price"]

cltv_c = df.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                        'Quantity': lambda x: x.sum(),
                                        'TotalPrice': lambda x: x.sum()})

cltv_c.columns = ["total_transaction", "total_unit", "total_price"]

## Average Order Value : 
cltv_c["average_order_value"] = cltv_c["total_price"] / cltv_c["total_transaction"]

## Purchase Frequency : 
### cltv_c.shape[0] = count customers 
cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0]

## Repeat Rate & Churn Rate : 
### less than 2 traces customers
cltv_c[cltv_c["total_transaction"] > 1] # birden fazla alışveriş 
cltv_c[cltv_c["total_transaction"] > 1].shape[0] # birden fazla alışveriş yapan müşteri sayısı

repeat_rate = cltv_c[cltv_c["total_transaction"] > 1].shape[0] / cltv_c.shape[0]
churn_rate = 1 - repeat_rate

## Profit Margin : 
cltv_c["profit_margin"] = cltv_c["total_price"] * 0.10

## Customer Value :
cltv_c["customer_value"] = cltv_c["average_order_value"] * cltv_c["purchase_frequency"]

## Customer Lifetime Value : 
cltv_c["cltv"] = (cltv_c["customer_value"] / churn_rate) * cltv_c["profit_margin"]
cltv_c.sort_values(by="cltv", ascending=False).head()

## Make a Segmentation : 
cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])
#cltv_c.sort_values(by="cltv", ascending=False).head()

cltv_c.groupby("segment").agg({"count", "mean", "sum"})
cltv_c.to_csv("cltv_c.csv")