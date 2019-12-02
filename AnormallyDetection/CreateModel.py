import pickle
import random

import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from fbprophet import Prophet

row = []

date_rng = pd.date_range(start='1/1/2018', end='1/02/2018', freq='S')
count = 0
for date in date_rng:
    temp = random.randrange(0, 60, 6)
    row.append((date, count, temp))
    count += 1
    # time.sleep(2.4)
    # pprint.pprint(row)

df = pd.DataFrame(row)
df.columns = ['ds', 'id', 'y']
# pprint.pprint(janith_df.head())
clean_df = df.drop(['id'], axis=1)
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
    print('fit_predict_model')
    print(dataframe)
    with open('anormaly_detection_model.pckl', 'wb') as fout:
        pickle.dump(m, fout)
    return None


fit_predict_model(clean_df)
