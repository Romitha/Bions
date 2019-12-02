import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics
import pickle

df = pd.read_csv('/home/janith/Documents/Python/Bions/Dow Jones Iron & Steel Historical Data.csv')
df = df[['Date', 'Price']].dropna()
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')
daily_df = df.resample('D').mean()
d_df = daily_df.reset_index().dropna()
d_df.columns = ['ds', 'y']

m = Prophet()
m.fit(d_df)
future = m.make_future_dataframe(periods=90)
forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']][-90:])

df_cv = cross_validation(m, horizon='90 days')
df_p = performance_metrics(df_cv)
print(df_p.head(5))

with open('forecast_model.pckl', 'wb') as fout:
    pickle.dump(m, fout)
