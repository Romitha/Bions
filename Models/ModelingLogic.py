import json

import matplotlib
from kafka import KafkaConsumer, TopicPartition
from json import loads
from sklearn.metrics import accuracy_score, f1_score, log_loss
from sklearn.model_selection import train_test_split

from Activity.KafkaActivity import KafkaActivity
from AnormallyDetection.DetectionActivity import DetectionActivity
from Models.SGDClassifierClass import SGDClassifierClass
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.style as style
import matplotlib.pyplot as plt

matplotlib.rcParams['font.weight'] = 3
matplotlib.rcParams['font.size'] = 10

style.use('bmh')


class ModelingLogic:
    @classmethod
    def consumer_train_model(cls, logger=None, topic_name=None, topic_offset=None):
        """ Consume the kafka message broker stream and partial fit the model """

        print("Consume the kafka message broker stream and partial fit the model")

        row_list = []
        ll_list = []
        accuracy_list = []
        f1_list = []

        selected_models = 0

        clf = SGDClassifierClass.initial_model(logger=logger)

        consumer = KafkaActivity.create_kafka_consumer(topic_name)
        print(consumer)

        counter = 1

        for message in consumer:
            print(message)
            message = message.value

            X = np.array(message['X'])
            y = np.array(message['y'])

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=2011, shuffle=True)

            if counter == 1:

                clf.partial_fit(X_train, y_train, classes=[0, 1])
                y_test_predict = clf.predict(X_test)

                clf_log_loss = log_loss(y_test, y_test_predict, labels=[0, 1])
                clf_acc_score = accuracy_score(y_test, y_test_predict)
                clf_f1_score = f1_score(y_test, y_test_predict)

                row_list.append(selected_models)
                ll_list.append(clf_log_loss)
                accuracy_list.append(clf_acc_score)
                f1_list.append(clf_f1_score)

            else:

                clf_temp = clf

                clf_temp.partial_fit(X_train, y_train, classes=[0, 1])
                y_test_predict = clf_temp.predict(X_test)

                clf_log_loss = log_loss(y_test, y_test_predict, labels=[0, 1])
                clf_acc_score = accuracy_score(y_test, y_test_predict)
                clf_f1_score = f1_score(y_test, y_test_predict)

                if clf_f1_score > (np.mean(f1_list) * 0.95):
                    # if clf_log_loss < (np.mean(ll_list) * 1.25) :

                    clf = clf_temp
                    selected_models += 1

                    logger.info(
                        f'Log loss : {format(clf_log_loss, "10.3f")};\tAccuracy score : {format(clf_acc_score, "10.3f")};\tF1 score : {format(clf_f1_score, "10.3f")}')

                    row_list.append(selected_models)
                    ll_list.append(clf_log_loss)
                    accuracy_list.append(clf_acc_score)
                    f1_list.append(clf_f1_score)

            counter += 1

            if counter == topic_offset:
                break

        consumer.close()

        df_metrics = pd.DataFrame.from_dict(
            {'row_list': row_list, 'll_list': ll_list, 'acc_list': accuracy_list, 'f1_list': f1_list})
        df_metrics['f1_ma'] = df_metrics['f1_list'].rolling(window=10).mean()
        df_metrics['ll_ma'] = df_metrics['ll_list'].rolling(window=10).mean()
        df_metrics['ac_ma'] = df_metrics['acc_list'].rolling(window=10).mean()

        logger.info(f'Number of trained routine : {selected_models}')

        if selected_models > 1000:
            subset_idx = 1000
        else:
            subset_idx = selected_models

        sns.lineplot(x="row_list", y="f1_ma", data=df_metrics.iloc[:subset_idx])
        cls.chart_save_image(plt=plt, f_size=(24, 8), left=0.05, right=0.97, bottom=0.05, top=0.97, wspace=0.0,
                             hspace=0.0,
                             fileName='./parital_fit_f1_metrics_plot.png')

        sns.lineplot(x="row_list", y="ll_ma", data=df_metrics.iloc[:subset_idx])
        cls.chart_save_image(plt=plt, f_size=(24, 8), left=0.05, right=0.97, bottom=0.05, top=0.97, wspace=0.0,
                             hspace=0.0,
                             fileName='./parital_fit_ll_metrics_plot.png')

        sns.lineplot(x="row_list", y="ac_ma", data=df_metrics.iloc[:subset_idx])
        cls.chart_save_image(plt=plt, f_size=(24, 8), left=0.05, right=0.97, bottom=0.05, top=0.97, wspace=0.0,
                             hspace=0.0,
                             fileName='./parital_fit_ac_metrics_plot.png')

        return None

    @classmethod
    def anormaly_detection(cls, logger=None, topic_name=None, topic_offset=None):
        """ Consume the kafka message broker stream and partial fit the model """

        print("Consume the kafka message broker stream and partial fit the model")
        consumer = KafkaActivity.create_kafka_consumer(topic_name)
        print(consumer)

        counter = 1

        for message in consumer:
            message = json.loads(message.value)
            X = message['X']
            y = message['y']
            print(message['X'])
            print(message['y'])

            df = DetectionActivity.create_data_frmae(X, y)
            pred = DetectionActivity.make_forecastign('/home/janith/Documents/Python/KafkaRealTimeML/AnormallyDetection/anormaly_detection_model.pckl', df)
            pred = DetectionActivity.detect_anomalies(pred)
            print(pred)

            counter += 1

            if counter == topic_offset:
                break

        consumer.close()

        return None

    @classmethod
    def chart_save_image(cls, plt=None, f_size=None, left=None, right=None, bottom=None, top=None, wspace=None,
                         hspace=None,
                         fileName=None):
        """ Save the chart image with the set of specific options """

        fig = plt.gcf()
        fig.set_size_inches(8, 4.5)  # To maintain the 16:9 aspect ratio;

        if f_size:
            fig.set_size_inches(f_size[0], f_size[1])

        # https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.subplots_adjust

        # left          = 0.125     # the left side of the subplots of the figure
        # right         = 0.9       # the right side of the subplots of the figure
        # bottom        = 0.125     # the bottom of the subplots of the figure
        # top           = 0.9       # the top of the subplots of the figure
        # wspace        = 0.0       # the amount of width reserved for blank space between subplots,
        #                           # expressed as a fraction of the average axis width
        # hspace        = 0.0       # the amount of height reserved for white space between subplots,
        #                           # expressed as a fraction of the average axis height

        plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
        plt.savefig(f'{fileName}')
        plt.clf()
