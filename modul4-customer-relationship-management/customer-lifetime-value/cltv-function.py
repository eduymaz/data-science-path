import pandas as pd

def create_cltv_c(dataframe, profit=0.10):
    """
    This function calculates the Customer Lifetime Value (CLTV) for each customer in the given dataframe.

    Parameters:
        dataframe (pd.DataFrame): The input dataframe containing customer transaction data.
        profit (float): The profit margin to be applied. Default is 10%.

    Returns:
        pd.DataFrame: A dataframe with CLTV and segmentation for each customer.
    """
    # Filter and preprocess the data
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[(dataframe["Quantity"] > 0)]
    dataframe.dropna(inplace=True)

    # Add a new column "TotalPrice"
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]

    # Group by Customer ID and aggregate metrics
    cltv_c = dataframe.groupby('Customer ID').agg({
        'Invoice': lambda x: x.nunique(),
        'Quantity': lambda x: x.sum(),
        'TotalPrice': lambda x: x.sum()
    })

    cltv_c.columns = ["total_transaction", "total_unit", "total_price"]

    # Calculate Average Order Value
    cltv_c["average_order_value"] = cltv_c["total_price"] / cltv_c["total_transaction"]

    # Calculate Purchase Frequency
    cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0]

    # Calculate Repeat Rate & Churn Rate
    repeat_rate = cltv_c[cltv_c["total_transaction"] > 1].shape[0] / cltv_c.shape[0]
    churn_rate = 1 - repeat_rate

    # Calculate Profit Margin
    cltv_c["profit_margin"] = cltv_c["total_price"] * profit

    # Calculate Customer Value
    cltv_c["customer_value"] = cltv_c["average_order_value"] * cltv_c["purchase_frequency"]

    # Calculate Customer Lifetime Value (CLTV)
    cltv_c["cltv"] = (cltv_c["customer_value"] / churn_rate) * cltv_c["profit_margin"]

    # Segment customers based on CLTV
    cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

    return cltv_c


