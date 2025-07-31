import pandas as pd
import datetime as dt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter

def replace_with_thresholds(data, variable):
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = data[variable].quantile(0.25)
    Q3 = data[variable].quantile(0.75)
    IQR = Q3 - Q1  # Interquartile Range

    # Calculate lower and upper bounds for outlier detection
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Replace outliers with NaN
    data[variable] = data[variable].where((data[variable] >= lower_bound) & (data[variable] <= upper_bound), other=pd.NA)

def create_cltv_p(dataframe, month=3):
    """
    This function calculates the Customer Lifetime Value (CLTV) for each customer using the BG-NBD and Gamma-Gamma models.

    Parameters:
        dataframe (pd.DataFrame): The input dataframe containing customer transaction data.
        month (int): The time period in months for which CLTV is calculated. Default is 3 months.

    Returns:
        pd.DataFrame: A dataframe with CLTV and segmentation for each customer.
    """
    # Data Preprocessing
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[(dataframe["Quantity"] > 0) & (dataframe["Price"] > 0)]

    # Replace outliers
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")

    # Add TotalPrice column
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]

    # Define today's date
    today_date = dt.datetime(2011, 12, 11)

    # Prepare data for BG-NBD model
    cltv_df = dataframe.groupby('Customer ID').agg({
        'InvoiceDate': [lambda InvoiceDate: (InvoiceDate.max() - InvoiceDate.min()).days,
                        lambda date: (today_date - date.min()).days],
        'Invoice': lambda Invoice: Invoice.nunique(),
        'TotalPrice': lambda TotalPrice: TotalPrice.sum()
    })

    cltv_df.columns = cltv_df.columns.droplevel(0)
    cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']

    cltv_df = cltv_df[(cltv_df['frequency'] > 1)]
    cltv_df["recency"] = cltv_df["recency"] / 7
    cltv_df["T"] = cltv_df["T"] / 7

    # Fit BG-NBD model
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(cltv_df['frequency'], cltv_df['recency'], cltv_df['T'])

    # Predict purchases for the given time period
    cltv_df[f"expected_purc_{month}_months"] = bgf.predict(4 * month, 
                                                             cltv_df['frequency'],
                                                             cltv_df['recency'],
                                                             cltv_df['T'])

    # Fit Gamma-Gamma model
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(cltv_df['frequency'], cltv_df['monetary'])

    # Calculate expected average profit
    cltv_df["expected_average_profit"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                                  cltv_df['monetary'])

    # Calculate CLTV
    cltv = ggf.customer_lifetime_value(bgf,
                                        cltv_df['frequency'],
                                        cltv_df['recency'],
                                        cltv_df['T'],
                                        cltv_df['monetary'],
                                        time=month,
                                        freq="W",  # Frequency of T
                                        discount_rate=0.01)

    cltv = cltv.reset_index()
    cltv_final = cltv_df.merge(cltv, on='Customer ID', how="left")

    # Segment customers based on CLTV
    cltv_final['segment'] = pd.qcut(cltv_final['clv'], 4, labels=['D', 'C', 'B', 'A'])

    return cltv_final
