"""This file contains the logger for DMming the bot"""
import os
import logging
from datetime import datetime as dt

if not os.path.exists('logs'):
    os.mkdir('logs')

today = dt.now().strftime('%Y%m%d')

LOG_FILENAME = f'logs/{today}.log'

logger = logging.getLogger("DMLogger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILENAME)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', '%m/%d/%y %H:%M:%S'))

logger.addHandler(file_handler)
