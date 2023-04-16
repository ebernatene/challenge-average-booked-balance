import pandas as pd
import numpy as np


def average_booked_balance_from(transactions: pd.DataFrame,
                                accounts: pd.DataFrame,
                                reference_timestamps: pd.DataFrame) -> pd.Series:
    """
    :param transactions: pandas dataframe containing the transactions from a collection of accounts
    :param accounts: pandas dataframe containing a collection of accounts together with their balance when they
        were first added to our systems.
    :param reference_timestamps: pandas dataframe with the timestamp a which to compute the average booked balance for
        each account. Different account might have different reference timestamps.
    :return:
        a pandas series where the index is a multindex containing the reference timestamp and the account id, and the
        values are the average booked balances, e.g

        index                               | value
        ('2022-01-12 23:59:59.999', 'ac_1') | 12.3
        ('2022-03-10 23:59:59.999', 'ac_2') | 26.8
    """
    WINDOW = 90 #days

    # Correct data type from string to datetime
    accounts["creation_timestamp"] = pd.to_datetime(
        accounts["creation_timestamp"],
        format='%Y-%m-%d %H:%M:%S.%f'
    )
    reference_timestamps["reference_timestamp"] = pd.to_datetime(
        reference_timestamps["reference_timestamp"],
        format='%Y-%m-%d %H:%M:%S.%f'
    )
    transactions["value_timestamp"] = pd.to_datetime(
        transactions["value_timestamp"],
        format='%Y-%m-%d %H:%M:%S.%f'
    )

    # Reference timestamp - 90 days
    reference_timestamps["init_reference_timestamp"] = reference_timestamps["reference_timestamp"] - pd.to_timedelta(WINDOW,unit="D")

    reference_timestamps = pd.merge(left=reference_timestamps,right=accounts,how="left",on="account_id")


    balance_avg = []
    # It's possible to make the code more performant using "apply" method compared to using a "for" loop.
    for idx in reference_timestamps.index:
        case = reference_timestamps.iloc[idx]

        # To filter transactions by account and between reference timestamp and 90 days before
        cond1 = transactions["account_id"] == case["account_id"]
        cond2 = transactions["value_timestamp"] >= case["init_reference_timestamp"]
        cond3 = transactions["value_timestamp"] <= case["reference_timestamp"]
        # Applying filter
        trans_id = transactions.loc[cond1 & cond2 & cond3].copy()

        # Sorting values by timestamp
        trans_id.sort_values(by="value_timestamp",ascending=True,inplace=True)

        # To filter transaction before creation timestamp
        cond4 = trans_id["value_timestamp"] <= case["creation_timestamp"]
        # Balance before the first transaction
        balance_init = case["balance_at_creation"] - trans_id.loc[cond4]["amount"].sum()
        # Balances after transactions
        trans_id["balance"] = trans_id["amount"].cumsum() + balance_init

        # Take the balance by day as the balance after the last transaction of the day  
        trans_id["date"] = trans_id["value_timestamp"].dt.date
        trans_day = trans_id.groupby("date").tail(1)

        # Creating daily balance for every days in the period
        timestamp = pd.date_range(
            start=case["init_reference_timestamp"] + pd.to_timedelta(1,unit="D"),
            end=case["reference_timestamp"],
            periods=WINDOW,
        )
        balance_day = pd.DataFrame({"timestamp":timestamp})
        balance_day["date"] = balance_day["timestamp"].dt.date
        balance_day = pd.merge(left=balance_day,right=trans_day[["date","balance"]],on="date",how="left")

        if np.isnan(balance_day.iloc[0]["balance"]):
            balance_day.at[0,"balance"] = balance_init
        
        balance_day.fillna(method='ffill',inplace=True)

        # Average is calculated (We EVER have 90 days of history!!! I'm not sure about this...) 
        balance_avg.append(balance_day["balance"].mean())

    reference_timestamps["average_booked_balance"] = balance_avg
    reference_timestamps.set_index(["reference_timestamp","account_id"],inplace=True)
    
    return reference_timestamps["average_booked_balance"]
