import pickle
import random

import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from fbprophet import Prophet


def make_forecastign(file, dataframe):
    with open(file, 'rb') as fin:
        m = pickle.load(fin)
    print('make_forecastign')
    print(m)
    forecast = m.predict(dataframe)
    forecast['fact'] = dataframe['y'].reset_index(drop=True)
    return forecast


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


row = ['2018-01-01 00:00:02', '200']
lst = [['2018-01-01 00:00:02', 40]]

df = pd.DataFrame(lst, columns=['ds', 'y'])
print('adoooooooooooooooooooo')
print(df)

pred = make_forecastign('anormaly_detection_model.pckl', df)
pred = detect_anomalies(pred)

print(pred)
