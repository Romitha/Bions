import random
import warnings
from time import time

import matplotlib
import matplotlib.style as style

from Activity.KafkaActivity import KafkaActivity
from Activity.LoggerActivity import LoggerActivity
from Models.ModelingLogic import ModelingLogic
from Models.SGDClassifierClass import SGDClassifierClass

matplotlib.rcParams['font.weight'] = 3
matplotlib.rcParams['font.size'] = 10

style.use('bmh')


def main(logger=None, kafka_path=None, loggerActivity=None):
    """ Main routine to call the entire process flow """
    print("Main routine to call the entire process flow")
    print(logger)
    print(kafka_path)
    # Main call --- Process starts

    loggerActivity.infoLog(f'', logger)
    loggerActivity.infoLog(f'{"-" * 20} List all kafka topics - starts here {"-" * 20}', logger)
    loggerActivity.infoLog(f'', logger)

    base_clf = SGDClassifierClass.initial_model(logger=logger)
    kafka_status = KafkaActivity.check_kafka_prcocess(logger=logger, loggerActivity=loggerActivity)
    print('kafka status - {}'.format(kafka_status))

    if kafka_status:
        loggerActivity.infoLog('Kafka stream is active', logger)
        topic_offset = KafkaActivity.get_topic_offset(logger=logger, topic_name='anomalydetection')
        loggerActivity.infoLog(f'Topic offset : {topic_offset}', logger)
        ModelingLogic.anormaly_detection(logger=logger, topic_name='anomalydetection', topic_offset=topic_offset)

    loggerActivity.infoLog(f'', logger)
    loggerActivity.infoLog(f'{"-" * 20} List all kafka topics - ends here {"-" * 20}', logger)
    loggerActivity.infoLog(f'', logger)

    # Main call --- Process ends

    return None


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    ts = time()

    random.seed(2011)

    kafka_path = KafkaActivity().get_kafka_path()
    print('kafka path {}'.format(kafka_path))
    loggerActivity = LoggerActivity('Consumer')
    Test_case = f'Kafka consumer code module : {loggerActivity.get_LOG_TS()}'
    Test_comment = '-' * len(Test_case)

    logger = loggerActivity.get_logger()
    print(logger)
    loggerActivity.infoLog(Test_comment, logger)
    loggerActivity.infoLog(Test_case, logger)
    loggerActivity.infoLog(Test_comment, logger)

    loggerActivity.delete_old_log_files(delete_flag=loggerActivity.get_DELETE_FLAG(), logger=logger,
                                        extension_list=loggerActivity.get_extension_list(),
                                        LOG_TS=loggerActivity.get_LOG_TS())
    main(logger=logger, kafka_path=kafka_path, loggerActivity=loggerActivity)

    loggerActivity.infoLog(Test_comment, logger)
    loggerActivity.infoLog(f'Code execution took {round((time() - ts), 4)} seconds', logger)
    loggerActivity.infoLog(Test_comment, logger)
