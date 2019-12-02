import pprint
import random
import subprocess
from builtins import print
from json import dumps
from json import loads
from time import sleep
import pandas as pd
import json
import datetime

from kafka import KafkaConsumer, TopicPartition
from kafka import KafkaProducer
from sklearn.preprocessing import MinMaxScaler

from Activity.GenerateData import GenerateData


class KafkaActivity:
    def __init__(self):
        self.kafka_path = '/home/janith/Documents/Python/kafka_2.11-2.2.0/'

    def get_kafka_path(self):
        return self.kafka_path

    @classmethod
    def check_kafka_prcocess(cls, logger=None, loggerActivity=None):
        """ Check if the kafka process is running or not """
        # All Kafka brokers must be assigned a broker.id. On startup a broker will create an ephemeral node in Zookeeper with a path of /broker/ids/$id ;

        cmd_string = f'echo dump | nc localhost 2181 | grep brokers'
        cmd_output = ''

        try:
            cmd_status = subprocess.check_output(cmd_string, stderr=subprocess.STDOUT, shell=True)
            cmd_output = cmd_status.decode('utf-8').split('\n')[0]
        except Exception as e:
            loggerActivity.infoLog(e, logger)

        logger.info(f'Kafka process status : ')

        if len(cmd_output) > 0:
            loggerActivity.infoLog(f'', logger)
            loggerActivity.infoLog(f'Running', logger)
            loggerActivity.infoLog(f'', logger)
            return 1
        else:
            loggerActivity.infoLog(f'', logger)
            loggerActivity.infoLog(f'Not Running', logger)
            loggerActivity.infoLog(f'', logger)
            return 0

        return None

    @classmethod
    def get_topic_offset(cls, logger=None, topic_name=None):
        """ To return the topic offset to break the continuous consumer listening to the message broker """
        print('To return the topic offset to break the continuous consumer listening to the message broker')

        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True,
                                 group_id='consumer_1_group_1',
                                 # The group_id is used by kafka to store the latest offset;
                                 value_deserializer=lambda x: loads(x.decode('utf-8'))
                                 )

        tp = TopicPartition(topic_name, 0)
        consumer.assign([tp])

        consumer.seek_to_end(tp)
        lastOffset = consumer.position(tp)
        consumer.close()

        return lastOffset

    @classmethod
    def create_kafka_consumer(cls, topic_name=None):
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            # group_id='consumer_1_group_2',   # The group_id is used by kafka to store the latest offset;
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
        return consumer

    @classmethod
    def list_topics(cls, logger=None, kafka_path=None, loggerActivity=None):
        """ Run the kafka shell command and return the list of available topics """
        print('Run the kafka shell command and return the list of available topics')

        # logger.info(f'kafka_path : {kafka_path}');

        cmd_string = f'{kafka_path}bin/kafka-topics.sh --list --zookeeper localhost:2181'
        list_of_topics = subprocess.check_output(cmd_string, stderr=subprocess.STDOUT, shell=True)
        list_of_topics = [i.lower() for i in list_of_topics.decode("utf-8").split("\n") if
                          len(i) > 0 and i.lower() != '__consumer_offsets']

        loggerActivity.infoLog(f'', logger)
        loggerActivity.infoLog('List of topics : ', logger)
        loggerActivity.infoLog(f'', logger)

        for topic in list_of_topics:
            loggerActivity.infoLog(f'{topic}', logger)

        loggerActivity.infoLog(f'', logger)

        return list_of_topics

    @classmethod
    def delete_all_topics(cls, logger=None, kafka_path=None, list_of_topics=None, loggerActivity=None):
        """ Run the kafka shell command to delete all listed topics """
        print('Run the kafka shell command to delete all listed topics')

        loggerActivity.infoLog(f'', logger)
        loggerActivity.infoLog('Delete all topics : ', logger)
        loggerActivity.infoLog(f'', logger)

        for topic in list_of_topics:
            cmd_string = f'{kafka_path}bin/kafka-topics.sh --zookeeper localhost:2181 -delete -topic {topic}'
            cmd_status = subprocess.check_output(cmd_string, stderr=subprocess.STDOUT, shell=True)
            cmd_output = cmd_status.decode('utf-8').split('\n')[0]

            loggerActivity.infoLog(f'{cmd_output}', logger)

        return None

    @classmethod
    def create_topic(cls, logger=None, kafka_path=None, topic=None, loggerActivity=None):
        """ Routine will create a new topic; assuming delete_all_topics will run before this routine """
        print('Routine will create a new topic; assuming delete_all_topics will run before this routine')

        cmd_string = f'{kafka_path}bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic {topic.lower()}'
        cmd_status = subprocess.check_output(cmd_string, stderr=subprocess.STDOUT, shell=True)
        cmd_output = cmd_status.decode('utf-8').split('\n')[0]

        loggerActivity.infoLog(f'', logger)
        loggerActivity.infoLog(f'{cmd_output}', logger)
        loggerActivity.infoLog(f'', logger)

        return None

    @classmethod
    def myconverter(cls, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    @classmethod
    def run_producer(cls, logger=None, topic=None, loggerActivity=None):
        """ Run a producer to put messages into a topic """
        print('Run a producer to put messages into a topic')

        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                 value_serializer=lambda x: dumps(x).encode('utf-8'))
        loggerActivity.infoLog(f'Publishing messages to the topic : {topic}', logger)

        date_rng = pd.date_range(start='1/1/2018', end='1/02/2018', freq='S')
        count = 0
        for date in date_rng:
            temp = random.randrange(0, 160, 6)
            count += 1
            # time.sleep(2.4)
            # pprint.pprint(row)

            data = {
                'X': [date, temp],
                'y': ['ds', 'y']
            }
            dump_data = json.dumps(data, default=cls.myconverter)
            producer.send(topic, value=dump_data)
            print(type(dump_data))
            pprint.pprint(dump_data)
            sleep(1)
            # sleep(5)

        loggerActivity.infoLog(f'Closing producer process; Total records generated is {format(record_count, "09,")}', logger)
        return None