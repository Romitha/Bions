import random
from builtins import print
from time import time
import pandas as pd
from Activity import LoggerActivity
from Activity.KafkaActivity import KafkaActivity


def main(logger=None, kafka_path=None, loggerActivity=None):
    """ Main routine to call the entire process flow """
    print('Main routine to call the entire process flow')

    # Main call --- Process starts

    loggerActivity.infoLog(f'', logger)
    loggerActivity.infoLog(f'{"-" * 20} List all kafka topics - starts here {"-" * 20}', logger)
    loggerActivity.infoLog(f'', logger)

    kafka_status = KafkaActivity.check_kafka_prcocess(logger=logger, loggerActivity=loggerActivity)
    print('kafka status - {}'.format(kafka_status))
    print('kafka path {}'.format(kafka_path))

    if kafka_status:
        list_of_topics = KafkaActivity.list_topics(logger=logger, kafka_path=kafka_path, loggerActivity=loggerActivity)
        print(list_of_topics)
        # *************************************** WARNING ***************************************;
        # Do not run the delete_all_topics in a production environment; it will delete all topics;
        # *************************************** WARNING ***************************************;
        if len(list_of_topics) > 0:
            KafkaActivity.delete_all_topics(logger=logger, kafka_path=kafka_path, list_of_topics=list_of_topics, loggerActivity=loggerActivity)
        # *************************************** WARNING ***************************************;
        # Do not run the delete_all_topics in a production environment; it will delete all topics;
        # *************************************** WARNING ***************************************;
        list_of_topics = KafkaActivity.list_topics(logger=logger, kafka_path=kafka_path, loggerActivity=loggerActivity)
        print("check weather topics are deleted")
        if len(list_of_topics) == 0:
            print("Topics are deleted")
        else:
            print("Cannot deleted Topics")
        KafkaActivity.create_topic(logger=logger, kafka_path=kafka_path, topic='anomalydetection', loggerActivity=loggerActivity)
        KafkaActivity.run_producer(logger=logger, topic='anomalydetection', loggerActivity=loggerActivity)
    logger.info(f'')
    logger.info(f'{"-" * 20} List all kafka topics - ends here {"-" * 20}')
    logger.info(f'')

    # Main call --- Process ends

    return None


if __name__ == "__main__":
    ts = time()
    random.seed(2011)
    kafka_path = KafkaActivity().get_kafka_path()
    print(kafka_path)
    loggerActivity = LoggerActivity('Producer')
    logger = loggerActivity.get_logger()
    print(logger)

    Test_case = f'Kafka producer code module : {loggerActivity.get_LOG_TS()}'
    Test_comment = '-' * len(Test_case)

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
