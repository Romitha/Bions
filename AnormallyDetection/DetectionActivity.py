import pickle
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)


class DetectionActivity:
    def __init__(self):
        print('DetectionActivity')

    @classmethod
    def create_data_frmae(cls, row, col):
        lst = [row]
        # print('create_data_frmae')
        # print(lst)
        # print(col)
        df = pd.DataFrame(lst, columns=col)
        return df

    @classmethod
    def make_forecastign(cls, file, dataframe):
        with open(file, 'rb') as fin:
            m = pickle.load(fin)
        print('make_forecastign')
        print(m)
        forecast = m.predict(dataframe)
        forecast['fact'] = dataframe['y'].reset_index(drop=True)
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