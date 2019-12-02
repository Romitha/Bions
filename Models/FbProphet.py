class FbProphet:
    def __init__(self):
        print('FbProphet')

    @classmethod
    def fit_predict_model(cls, dataframe, interval_width=0.99, changepoint_range=0.8):
        m = Prophet(daily_seasonality=False, yearly_seasonality=False, weekly_seasonality=False,
                    seasonality_mode='multiplicative',
                    interval_width=interval_width,
                    changepoint_range=changepoint_range)
        m = m.fit(dataframe)

        forecast = m.predict(dataframe)
        forecast['fact'] = dataframe['y'].reset_index(drop=True)
        # print('Displaying Prophet plot')
        fig1 = m.plot(forecast)
        return forecast

    @classmethod
    def detect_anomalies(cls, forecast):
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
