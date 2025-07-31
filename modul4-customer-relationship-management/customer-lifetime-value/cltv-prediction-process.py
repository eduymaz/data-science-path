# DATA : https://archive.ics.uci.edu/dataset/502/online+retail+ii

#pip install lifetimes
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%4f' % x)
from sklearn.preprocessing import MinMaxScaler


def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01) # Todo
    quartile3 = dataframe[variable].quantile(0.99) # Todo
    interquartile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquartile_range
    low_limit = quartile1 - 1.5 * interquartile_range

    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit # can be closed.
    dataframe.loc[(dataframe[variable] < up_limit), variable] = up_limit


df_ = pd.read_excel('../data/online_retail_II.xlsx', sheet_name="Year 2010-2011")
df = df_.copy()

df.describe().T

df.isnull().sum()

# data preprocess : 
df.dropna(inplace=True)

df = df[~df["Invoice"].str.contains("C", na=False)]
df = df[df["Quantity"] > 0]
df = df[df["Price"] > 0]

replace_with_thresholds(df, "Quantity")
replace_with_thresholds(df, "Price")

df["TotalPrice"] = df["Quantity"] * df["Price"]

today_date = dt.datetime(2011, 12, 11)


# Prepare a Data for BG-NBD Models 
###
# recency : Son satın alma üzerinden geçen zaman. Haftalık (kullanıcı özelinde)
# monetary = satın alma başına ortalama kazanç
# T : Müşterinin yaşı.Haftalık (analiz tarihinden ne kadar süre önce ilk satın alma yapılmış)
# 

cltv_df = df.groupby('Customer ID').agg({'InvoiceDate': [lambda InvoiceDate: (InvoiceDate.max() - InvoiceDate.min()).days,
                                                         lambda date: (today_date - date.min()).days],
                                                         'Invoice': lambda Invoice: Invoice.nunique(),
                                                         'TotalPrice': lambda TotalPrice: TotalPrice.sum()})



cltv_df.columns = cltv_df.columns.droplevel(0)
cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']

cltv_df = cltv_df[(cltv_df['frequency'] > 1)]
cltv_df["recency"] = cltv_df["recency"] / 7
cltv_df["T"] = cltv_df["T"] / 7

# Establishment of BG-NBD Models 

bgf = BetaGeoFitter(penalizer_coef=0.001)

bgf.fit(cltv_df['frequency'],
        cltv_df['recency'],
        cltv_df['T'])

# expectation : 10 custoemrs to purchase on 1 week

bgf.conditional_expected_number_of_purchases_up_to_time(1,
                                                        cltv_df['frequency'],
                                                        cltv_df['recency'],
                                                        cltv_df['T'].sort_values(ascending=False).head(10))

# or we can write predict function : 

bgf.predict(1, 
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T'].sort_values(ascending=False).head(10))

cltv_df["expected_purc_1_week"] = bgf.predict(1, 
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T'])


# expectation : 10 custoemrs to purchase on 4 week


bgf.predict(1, 
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T'].sort_values(ascending=False).head(10))

cltv_df["expected_purc_4_week"] = bgf.predict(4,  # added week info
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T'])


bgf.predict(4, 
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sum()

plot_period_transactions(bgf)
plt.show()

# expectation : 10 customers to purchase on 3 months  ->

cltv_df["expected_purc_3_months"] = bgf.predict(4 * 3,  # added week info
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T'])


# Establishment of GAMMA - GAMMA Model

ggf = GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(cltv_df['frequency'], cltv_df['monetary'])

ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary'].sort_values(ascending=False).head(10))


cltv_df["expected_average_profit"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary'])


cltv_df.sort_values("expected_average_profit", ascending=False).head(10)
 
 ##########################################
 # Calculation of CLTV with BG-NBD and GG Model

cltv = ggf.customer_lifetime_value(bgf,
                                    cltv_df['frequency'],
                                    cltv_df['recency'],
                                    cltv_df['T'],
                                    cltv_df['monetary'],
                                    time=3,
                                    freq="W",  # T'nin frekans bilgisi 
                                    discount_rate=0.01)

cltv.head()

cltv = cltv.reset_index()

cltv_final = cltv_df.merge(cltv, on='Customer ID', how="left")
cltv_final.sort_values(by="clv", ascending=False).head(10)

 ##########################################
# NOT :  BG NBD düzenli müşterinin recency arttıkca satın alma olasılığı yükseliyordur!
 ##########################################

# Make a Segmentation according to CLTV

cltv_final
cltv_final['segment'] = pd.qcut(cltv_final['clv'], 4, labels=['D', 'C', 'B', 'A'])

#cltv_final.sort_values(by='scaled_clv', ascending=False).head(50)
cltv_final.groupby("segment").agg({"count", "mean", "sum"})