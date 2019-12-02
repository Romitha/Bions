import datetime
import logging
import os
import random
import subprocess
import warnings
from time import time
import numpy as np
import pandas as pd
import seaborn as sns


class LoggerActivity:
    def __init__(self, log_file_name):
        self.log_filename = log_file_name + datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S') + '.log'
        self.LOG_TS = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        self.LOG_LEVEL = logging.DEBUG
        self.DELETE_FLAG = True
        self.extension_list = ['.log', '.pkl']
        # (LogLevel : Numeric_value) : (CRITICAL : 50) (ERROR : 40) (WARNING : 30) (INFO : 20) (DEBUG : 10) (NOTSET : 0)
        self.logger = logging.getLogger(log_file_name)
        self.logger.setLevel(self.LOG_LEVEL)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%d/%m %H:%M:%S')
        self.fh = logging.FileHandler(filename=self.log_filename)
        self.fh.setLevel(self.LOG_LEVEL)
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def get_logger(self):
        return self.logger

    def get_LOG_TS(self):
        return self.LOG_TS

    def get_LOG_LEVEL(self):
        return self.LOG_LEVEL

    def get_DELETE_FLAG(self):
        return self.DELETE_FLAG

    def get_extension_list(self):
        return self.extension_list

    @classmethod
    def infoLog(cls, information, logger=None):
        logger.info(information)
        return None

    @classmethod
    def delete_old_log_files(cls, delete_flag=False, logger=None, extension_list=None, LOG_TS=None):
        """ Function to delete the old log files; cleanup process """
        print('Function to delete the old log files; cleanup process')
        directory = './'
        file_list = os.listdir(directory)

        if delete_flag:
            logger.info('DELETE_FLAG is set to true')
            logger.info('All previous logfiles will be deleted')

            logger.info(f'')
            logger.info(f'{"-" * 20} File deletion starts here {"-" * 20}')
            logger.info(f'')

            for item in file_list:
                ext_flag = [item.endswith(i) for i in extension_list]
                # logger.info(f'{ext_flag} | {item} | {np.sum(ext_flag)} | {fileName in item}');
                if np.sum(ext_flag) and (LOG_TS not in item):
                    os.remove(os.path.join(directory, item))
                    logger.info(f'Deleted file : {item}')

            logger.info(f'')
            logger.info(f'{"-" * 20} File deletion ends here {"-" * 20}')
            logger.info(f'')
            print('File deletion ends here')

        return None
