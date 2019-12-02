import pprint

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from fbprophet import Prophet
from datetime import datetime
import random
import time
import pickle

row = []

date_rng = pd.date_range(start='1/1/2018', end='1/01/2018', freq='S')
count = 0
for date in date_rng:
    temp = random.randrange(0, 60, 6)
    row.append((date, count, temp))
    count += 1
    # time.sleep(2.4)
    # pprint.pprint(row)

janith_df = pd.DataFrame(row)
janith_df.columns = ['ds', 'id', 'y']
pprint.pprint(janith_df.head())

# data = np.loadtxt("/home/janith/Documents/Python/Bions/sunspots.txt", float)
# data_as_frame = pd.DataFrame(data, columns=['Months', 'SunSpots'])
# print(data_as_frame.tail(10))
#
# data_as_frame['ds'] = data_as_frame['Months'].astype(int)
# print(data_as_frame.head())
#
# data_as_frame['time_stamp'] = data_as_frame.apply(
#     lambda x: (pd.Timestamp('1749-01-01') + pd.DateOffset(months=int(x['ds']))), axis=1)
clean_df = janith_df.drop(['id'], axis=1)

# print(clean_df.head())

clean_df.columns = ['ds', 'y']


# print('----------------clean DF--------------------------')
# print(clean_df)


def fit_predict_model(dataframe, interval_width=0.99, changepoint_range=0.8):
    m = Prophet(daily_seasonality=False, yearly_seasonality=False, weekly_seasonality=False,
                seasonality_mode='multiplicative',
                interval_width=interval_width,
                changepoint_range=changepoint_range)
    m = m.fit(dataframe)

    forecast = m.predict(dataframe)
    forecast['fact'] = dataframe['y'].reset_index(drop=True)
    # print('Displaying Prophet plot')
    # fig1 = m.plot(forecast)
    with open('predict_model.pckl', 'wb') as fout:
        pickle.dump(m, fout)
    return forecast


pred = fit_predict_model(clean_df)
print(type(pred))


def detect_anomalies(forecast):
    forecasted = forecast[['ds', 'trend', 'yhat', 'yhat_lower', 'yhat_upper', 'fact']].copy()
    # forecast['fact'] = df['y']

    forecasted['anomaly'] = 0
    forecasted.loc[forecasted['fact'] > forecasted['yhat_upper'], 'anomaly'] = 1
    forecasted.loc[forecasted['fact'] < forecasted['yhat_lower'], 'anomaly'] = -1

    # anomaly importances
    forecasted['importance'] = 0
    forecasted.loc[forecasted['anomaly'] == 1, 'importance'] = \
        (forecasted['fact'] - forecasted['yhat_upper']) / forecast['fact']
    forecasted.loc[forecasted['anomaly'] == -1, 'importance'] = \
        (forecasted['yhat_lower'] - forecasted['fact']) / forecast['fact']

    return forecasted


pred = detect_anomalies(pred)

print(pred)
